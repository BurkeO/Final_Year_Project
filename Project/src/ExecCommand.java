import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class ExecCommand
{
    private Semaphore outputSem;
    private Semaphore errorSem;
    private Process p;

    private class OutputReader extends Thread
    {
        public OutputReader()
        {
            try
            {
                outputSem = new Semaphore(1);
                outputSem.acquire();
            }
            catch (InterruptedException e)
            {
                e.printStackTrace();
            }
        }

        public void run()
        {
            try
            {
                StringBuilder readBuffer = new StringBuilder();
                BufferedReader isr = new BufferedReader(new InputStreamReader(p.getInputStream()));
                String buff;
                while ((buff = isr.readLine()) != null)
                {
                    readBuffer.append(buff);
                }
                outputSem.release();
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }
    }

    private class ErrorReader extends Thread
    {
        public ErrorReader()
        {
            try
            {
                errorSem = new Semaphore(1);
                errorSem.acquire();
            }
            catch (InterruptedException e)
            {
                e.printStackTrace();
            }
        }

        public void run()
        {
            try
            {
                StringBuilder readBuffer = new StringBuilder();
                BufferedReader isr = new BufferedReader(new InputStreamReader(p.getErrorStream()));
                String buff;
                while ((buff = isr.readLine()) != null)
                {
                    readBuffer.append(buff);
                }
                errorSem.release();
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }
    }

    public ExecCommand(String command)
    {
        try
        {
            p = Runtime.getRuntime().exec(makeArray(command));
            new OutputReader().start();
            new ErrorReader().start();
            p.waitFor();
        }
        catch (IOException | InterruptedException e)
        {
            e.printStackTrace();
        }
    }

    private String[] makeArray(String command)
    {
        ArrayList<String> commandArray = new ArrayList<>();
        StringBuilder buff = new StringBuilder();
        boolean lookForEnd = false;
        for (int i = 0; i < command.length(); i++)
        {
            if (lookForEnd)
            {
                if (command.charAt(i) == '\"')
                {
                    if (buff.length() > 0)
                        commandArray.add(buff.toString());
                    buff = new StringBuilder();
                    lookForEnd = false;
                }
                else
                {
                    buff.append(command.charAt(i));
                }
            }
            else
            {
                if (command.charAt(i) == '\"')
                {
                    lookForEnd = true;
                }
                else if (command.charAt(i) == ' ')
                {
                    if (buff.length() > 0)
                        commandArray.add(buff.toString());
                    buff = new StringBuilder();
                }
                else
                {
                    buff.append(command.charAt(i));
                }
            }
        }
        if (buff.length() > 0)
            commandArray.add(buff.toString());

        String[] array = new String[commandArray.size()];
        for (int i = 0; i < commandArray.size(); i++)
        {
            array[i] = commandArray.get(i);
        }

        return array;
    }
}
import be.tarsos.dsp.AudioDispatcher;
import be.tarsos.dsp.io.TarsosDSPAudioInputStream;
import be.tarsos.dsp.io.jvm.JVMAudioInputStream;

import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.UnsupportedAudioFileException;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

public class ProjectMain
{


    public static void main(String[] args)
    {
        File initialFile = new File("D:/Users/Owen/Final_Year_Project/recordings/Ireland/Common_Wood_Pigeon/372363/XC372363-Columba_palumbus_Dublin_1518.mp3");
        try
        {
            AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(initialFile);
            TarsosDSPAudioInputStream tarsosDSPAudioInputStream = new JVMAudioInputStream(audioInputStream);
            AudioDispatcher dispatcher = new AudioDispatcher(tarsosDSPAudioInputStream, 2046, 2046);
            dispatcher.run();
        }
        catch (UnsupportedAudioFileException | IOException e)
        {
            e.printStackTrace();
        }

    }
}

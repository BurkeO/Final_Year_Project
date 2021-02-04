import jm.util.Read;
import me.gommeantilegit.sonopy.Sonopy;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

import java.io.File;
import java.io.IOException;
import java.nio.file.FileSystemException;

//import be.tarsos.dsp.mfcc.MFCC;


public class ProjectMain
{
    private static void splitWavFiles() throws FileSystemException
    {
        File dir = new File("birdsong");
        File[] directoryListing = dir.listFiles();
        if (directoryListing != null)
        {
            for (File child : directoryListing)
            {
                File[] audioFilesArray = child.listFiles();
                assert audioFilesArray != null;
                for (File audioFile : audioFilesArray)
                {
                    System.out.println("Working on " + audioFile.getName());
                    String parentPath = audioFile.getParentFile().getAbsolutePath();
                    String filename = parentPath + "\\" + audioFile.getName();
                    int pos = filename.lastIndexOf(".");
                    if (pos > 0)
                    {
                        filename = filename.substring(0, pos);
                    }
                    new ExecCommand("ffmpeg -i " + audioFile.getAbsolutePath() +
                            " -f segment -segment_time 3 -c copy " + filename + "%03d.wav");
                    boolean wasDeleted = audioFile.delete();
                    if (!wasDeleted)
                    {
                        throw new FileSystemException("Couldn't delete" + audioFile.toString());
                    }
                }
            }
        }
        else
        {
            throw new FileSystemException("Not a folder");
        }
    }

    private static void generateImages() throws FileSystemException
    {
        File dir = new File("birdsong");
        File[] directoryListing = dir.listFiles();
        if (directoryListing != null)
        {
            for (File child : directoryListing)
            {
                File[] audioFilesArray = child.listFiles();
                assert audioFilesArray != null;
                for (File audioFile : audioFilesArray)
                {
                    System.out.println("Making image for" + audioFile.getName());
                    System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
                    float[] audio = Read.audio(audioFile.getPath());
                    Sonopy sonopy = new Sonopy(44100, 256, 128, 256,
                            128);
                    float[][] mels = sonopy.melSpec(audio);

                    System.out.println(mels.length + ", " + mels[0].length);

                    double[][] spectrogram = new double[mels.length][mels[0].length];

                    for (int i = 0; i < mels.length; i++)
                    {
                        for (int j = 0; j < mels[0].length; j++)
                            spectrogram[i][j] = mels[i][j];
                    }
                    double[] doubleAudio = new double[audio.length];
                    for (int i = 0; i < doubleAudio.length; i++)
                    {
                        doubleAudio[i] = audio[i];
                    }

                    double[][] power = ProjectMain.powerToDb(spectrogram);

                    Mat image = new Mat(spectrogram.length, spectrogram[0].length, CvType.CV_64FC1);
                    for (int row = 0; row < spectrogram.length; row++)
                    {
                        for (int col = 0; col < spectrogram[0].length; col++)
                        {
                            image.put(row, col, spectrogram[row][col]);
                        }
                    }
                    Core.normalize(image, image, 0, 255, Core.NORM_MINMAX);
                    String parentPath = audioFile.getParentFile().getAbsolutePath();
                    String filename = parentPath + "\\" + audioFile.getName();
                    int pos = filename.lastIndexOf(".");
                    if (pos > 0)
                    {
                        filename = filename.substring(0, pos);
                    }
                    Imgcodecs.imwrite(filename+".png", image);
                    boolean wasDeleted = audioFile.delete();
                    if(!wasDeleted)
                    {
                        throw new FileSystemException("Couldn't delete file");
                    }

                }
            }
        }
        else
        {
            throw new FileSystemException("Not a folder");
        }
    }

    public static double[][] powerToDb(double[][] melS)
    {
        //Convert a power spectrogram (amplitude squared) to decibel (dB) units
        //  This computes the scaling ``10 * log10(S / ref)`` in a numerically
        //  stable way.
        double[][] log_spec = new double[melS.length][melS[0].length];
        double maxValue = -100;
        for (int i = 0; i < melS.length; i++)
        {
            for (int j = 0; j < melS[0].length; j++)
            {
                double magnitude = Math.abs(melS[i][j]);
                if (magnitude > 1e-10)
                {
                    log_spec[i][j] = 10.0 * log10(magnitude);
                }
                else
                {
                    log_spec[i][j] = 10.0 * (-10);
                }
                if (log_spec[i][j] > maxValue)
                {
                    maxValue = log_spec[i][j];
                }
            }
        }
        //set top_db to 80.0
        for (int i = 0; i < melS.length; i++)
        {
            for (int j = 0; j < melS[0].length; j++)
            {
                if (log_spec[i][j] < maxValue - 80.0)
                {
                    log_spec[i][j] = maxValue - 80.0;
                }
            }
        }
        //ref is disabled, maybe later.
        return log_spec;
    }

    private static double log10(double value)
    {
        return Math.log(value) / Math.log(10);
    }

    public static void main(String[] args) throws IOException, InterruptedException
    {
//        File f = new File("D:/Users/Owen/Final_Year_Project/birdsong/Common_Wood_Pigeon/Common_Wood_Pigeon_0.wav");
//
//        String file_path = f.getAbsolutePath();
//
//        System.out.println("Converting " + file_path + " ...");
//        String output_image_path = "temp.png";
//        File outputFile = new File(output_image_path);
//
//        MelSpectrogram melGram = new MelSpectrogram();
//        melGram.setOutputFrameWidth(MelSpectrogram.Width);
//        melGram.setOutputFrameHeight(MelSpectrogram.Height);
//        BufferedImage image = null;
//        try
//        {
//            image = melGram.convertAudio(f);
//        }
//        catch (UnsupportedAudioFileException | LineUnavailableException e)
//        {
//            e.printStackTrace();
//        }
//
//        assert image != null;
//        ImageIO.write(image, "png", outputFile);


//        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
//        float[] audio = Read.audio("src/out000.wav");
//        Sonopy sonopy = new Sonopy(44100, 256, 128, 256, 128);
//        float[][] mels = sonopy.melSpec(audio);
//
//        System.out.println(mels.length + ", " + mels[0].length);
//
//        double[][] spectrogram = new double[mels.length][mels[0].length];
//
//        for (int i = 0; i < mels.length; i++)
//        {
//            for (int j = 0; j < mels[0].length; j++)
//                spectrogram[i][j] = mels[i][j];
//        }
//        double[] doubleAudio = new double[audio.length];
//        for (int i = 0; i < doubleAudio.length; i++)
//        {
//            doubleAudio[i] = audio[i];
//        }
//
//        double[][] power = ProjectMain.powerToDb(spectrogram);
//
//        Mat image = new Mat(spectrogram.length, spectrogram[0].length, CvType.CV_64FC1);
//        for (int row = 0; row < spectrogram.length; row++)
//        {
//            for (int col = 0; col < spectrogram[0].length; col++)
//            {
//                image.put(row, col, spectrogram[row][col]);
//            }
//        }
//        Core.normalize(image, image, 0, 255, Core.NORM_MINMAX);
//        Imgcodecs.imwrite("power_spec.jpg", image);
        splitWavFiles();
        generateImages();
    }
}

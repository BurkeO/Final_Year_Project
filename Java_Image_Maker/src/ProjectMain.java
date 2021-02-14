import be.tarsos.dsp.AudioDispatcher;
import be.tarsos.dsp.AudioEvent;
import be.tarsos.dsp.AudioProcessor;
import be.tarsos.dsp.io.TarsosDSPAudioFormat;
import be.tarsos.dsp.io.UniversalAudioInputStream;
import jm.util.Read;
import me.gommeantilegit.sonopy.Sonopy;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.Rect;
import org.opencv.imgcodecs.Imgcodecs;

import javax.imageio.ImageIO;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.FileSystemException;
import java.util.Arrays;
import java.util.Objects;

import org.tensorflow.Operand;
import org.tensorflow.Output;
import org.tensorflow.op.Scope;
import org.tensorflow.op.audio.Mfcc;
import org.tensorflow.op.audio.DecodeWav;
import org.tensorflow.op.io.ReadFile;

import be.tarsos.dsp.mfcc.MFCC;

import static org.opencv.imgcodecs.Imgcodecs.imread;
import static org.opencv.imgcodecs.Imgcodecs.imwrite;


public class ProjectMain
{
    static{
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    }

    private static void splitWavFiles(File wavFileDirectory, File outputDirectory) throws FileSystemException
    {
        File[] speciesDirectoryArray = wavFileDirectory.listFiles();
        assert speciesDirectoryArray != null;
        File speciesOutputDirectory = null;
        int minCount = Integer.MAX_VALUE;
        for (int i = 0; i < speciesDirectoryArray.length; i++)
        {
            File speciesDirectory = speciesDirectoryArray[i];
            File[] audioFilesArray = speciesDirectory.listFiles();
            assert audioFilesArray != null;
            int count = 0;
            for (File audioFile : audioFilesArray)
            {
                if(count > minCount)
                    break;
                System.out.println("Working on " + audioFile.getName());
                speciesOutputDirectory = new File(outputDirectory.getAbsolutePath() + "\\" + speciesDirectory.getName());
                if (!speciesOutputDirectory.exists())
                {
                    speciesOutputDirectory.mkdirs();
                }
                String filename = speciesOutputDirectory.getAbsolutePath() + "\\" + audioFile.getName();
                String normFilename = filename + "_norm";
                String passFilename = normFilename + "_pass";
                String noiseFilename = passFilename + "_afftdn";
                String silenceFilename = noiseFilename + "_silence";
                int pos = filename.lastIndexOf(".");
                if (pos > 0)
                {
                    filename = filename.substring(0, pos);
                }
                new ExecCommand("ffmpeg -i " + audioFile.getAbsolutePath() +
                        " -af loudnorm " + normFilename + ".wav");
                //TODO figure this one out, doesnt seem to do much
                new ExecCommand("ffmpeg -i " + normFilename + ".wav" +
                        " -af \"highpass=f=22, lowpass=f=9000\" " + passFilename + ".wav");
                //
                new ExecCommand("ffmpeg -i " + passFilename + ".wav" +
                        " -af afftdn " + noiseFilename + ".wav");
                //
                new ExecCommand("ffmpeg -i " + noiseFilename + ".wav" +
                        " -af silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-46dB " + silenceFilename + ".wav");
                //
                new ExecCommand("ffmpeg -i " + silenceFilename + ".wav" +
                        " -f segment -segment_time 3 -c copy " + filename + "%03d.wav");
                //
                boolean normDeleted = new File(normFilename + ".wav").delete();
                boolean passDeleted = new File(passFilename + ".wav").delete();
                boolean noiseDeleted = new File(noiseFilename + ".wav").delete();
                boolean silenceDeleted = new File(silenceFilename + ".wav").delete();
                //
                if(!normDeleted || !passDeleted || !noiseDeleted || !silenceDeleted)
                    throw new FileSystemException("Failed to deleted file");
                count =  speciesOutputDirectory.listFiles().length;
//                    boolean wasDeleted = audioFile.delete();
//                    if (!wasDeleted)
//                    {
//                        throw new FileSystemException("Couldn't delete" + audioFile.toString());
//                    }
            }
            if(i == 0 || count < minCount)
            {
                minCount = count;
            }
        }
        for(File speciesOutputFile : speciesOutputDirectory.getParentFile().listFiles())
        {
            File[] wavFiles = speciesOutputFile.listFiles();
            int numberToDelete = wavFiles.length - minCount;
            for(int i = 0; i < numberToDelete; i++)
            {
                wavFiles[i].delete();
            }
        }
    }

    private static void generateImages(File wavFileDirectory, File outputDirectory) throws FileSystemException
    {
        File[] speciesDirectoryArray = wavFileDirectory.listFiles();
        if (speciesDirectoryArray != null)
        {
            for (File speciesDirectory : speciesDirectoryArray)
            {
                File[] audioFilesArray = speciesDirectory.listFiles();
                assert audioFilesArray != null;
                for (File audioFile : audioFilesArray)
                {
//                    System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
//                    float[] audio = Read.audio(audioFile.getPath());
//                    Sonopy sonopy = new Sonopy(44100, 256, 128, 256,
//                            128);
//                    float[][] mels = sonopy.melSpec(audio);
//
//                    System.out.println(mels.length + ", " + mels[0].length);
//
//                    double[][] spectrogram = new double[mels.length][mels[0].length];
//
//                    for (int i = 0; i < mels.length; i++)
//                    {
//                        for (int j = 0; j < mels[0].length; j++)
//                            spectrogram[i][j] = mels[i][j];
//                    }
//                    double[] doubleAudio = new double[audio.length];
//                    for (int i = 0; i < doubleAudio.length; i++)
//                    {
//                        doubleAudio[i] = audio[i];
//                    }
//
//                    double[][] power = ProjectMain.powerToDb(spectrogram);
//
//                    Mat image = new Mat(spectrogram.length, spectrogram[0].length, CvType.CV_64FC1);
//                    for (int row = 0; row < spectrogram.length; row++)
//                    {
//                        for (int col = 0; col < spectrogram[0].length; col++)
//                        {
//                            image.put(row, col, spectrogram[row][col]);
//                        }
//                    }
//                    Core.normalize(image, image, 0, 255, Core.NORM_MINMAX);
                    File speciesOutputDirectory = new File(outputDirectory.getAbsolutePath() + "\\" + speciesDirectory.getName());
                    if(!speciesOutputDirectory.exists())
                    {
                        speciesOutputDirectory.mkdirs();
                    }
                    String filename = speciesOutputDirectory.getAbsolutePath() + "\\" + audioFile.getName();
                    int pos = filename.lastIndexOf(".");
                    if (pos > 0)
                    {
                        filename = filename.substring(0, pos);
                    }
                    //Imgcodecs.imwrite(filename+".png", image);
                    //to start from left off
                    if(new File(filename+".png").exists())
                        continue;
                    //
                    System.out.println("Making image for " + audioFile.getName());
                    new ExecCommand("ffmpeg -i " + audioFile.getAbsolutePath() +
                            " -lavfi showspectrumpic=s=600x960:stop=10000 " + filename + ".png");
                    //https://www.wearethefirehouse.com/aspect-ratio-cheat-sheet
                    Mat img = Imgcodecs.imread(filename+".png", Imgcodecs.IMREAD_COLOR);
                    int borderWidth = 156;
                    int borderHeigth = 60;
                    Rect crop = new Rect(borderWidth, borderHeigth, img.width()-(borderWidth*2), img.height()-(borderHeigth*2));
                    Mat croppedImage = new Mat(img, crop);
                    //new File(filename+".png").delete();
                    imwrite(filename+"_cropped.png", croppedImage);
                    //TODO remove
                    break;
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

    public static void main(String[] args) throws IOException, InterruptedException, UnsupportedAudioFileException
    {
//        File f = new File("D:/Users/Owen/Final_Year_Project/Dev_Recordings_Split_Wavs/Common_Wood_Pigeon/Common_Wood_Pigeon_0000.wav");
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
//        float[] audio = Read.audio("D:/Users/Owen/Final_Year_Project/Dev_Recordings_Split_Wavs/Common_Wood_Pigeon/Common_Wood_Pigeon_0000.wav");
//        Sonopy sonopy = new Sonopy(44100, 1024, 512, 256, 128);
//        float[][] mels = sonopy.melSpec(audio);
//
//        System.out.println(mels.length + ", " + mels[0].length);

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

//        Mat imageMat = new Mat(spectrogram.length, spectrogram[0].length, CvType.CV_64FC1);
//        for (int row = 0; row < spectrogram.length; row++)
//        {
//            for (int col = 0; col < spectrogram[0].length; col++)
//            {
//                imageMat.put(row, col, spectrogram[row][col]);
//            }
//        }
//        Core.normalize(imageMat, imageMat, 0, 255, Core.NORM_MINMAX);
//        Imgcodecs.imwrite("power_spec.jpg", imageMat);
//        Mat imageMat = new Mat(mels.length, mels[0].length, CvType.CV_64FC1);
//        for (int row = 0; row < mels.length; row++)
//        {
//            for (int col = 0; col < mels[0].length; col++)
//            {
//                imageMat.put(row, col, mels[row][col]);
//            }
//        }
//        Core.normalize(imageMat, imageMat, 0, 255, Core.NORM_MINMAX);
//        Imgcodecs.imwrite("mels.jpg", imageMat);
//        int sampleRate = 44100;
//        int bufferSize = 1024;
//        int bufferOverlap = 128;
//        InputStream inStream = new FileInputStream("D:/Users/Owen/Final_Year_Project/Dev_Recordings_Split_Wavs/Common_Wood_Pigeon/Common_Wood_Pigeon_0000.wav");
//        AudioDispatcher dispatcher = new AudioDispatcher(new UniversalAudioInputStream(inStream, new TarsosDSPAudioFormat(sampleRate, bufferSize, 1, true, false)), bufferSize, bufferOverlap);
//
//        final MFCC mfcc = new MFCC(bufferSize, sampleRate, 40, 128, 0, 10000);
//        dispatcher.addAudioProcessor(mfcc);
//        dispatcher.addAudioProcessor(new AudioProcessor() {
//
//            @Override
//            public void processingFinished() {
//            }
//
//            @Override
//            public boolean process(AudioEvent audioEvent) {
//                return true;
//            }
//        });
//        dispatcher.run();
//        float[] mfccArray = mfcc.getMFCC();
//        int i = 0;

        int i = 0;
        splitWavFiles(new File("D:\\Users\\Owen\\Final_Year_Project\\Dev_Test"),
                new File("D:\\Users\\Owen\\Final_Year_Project\\Dev_Test_Split_wavs"));
//        generateImages(new File("D:\\Users\\Owen\\Final_Year_Project\\Dev_Test_Split_wavs"),
//                new File("D:\\Users\\Owen\\Final_Year_Project\\Dev_Test_Images"));
    }
}

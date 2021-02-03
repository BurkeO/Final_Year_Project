import be.tarsos.dsp.AudioDispatcher;
import be.tarsos.dsp.AudioEvent;
import be.tarsos.dsp.AudioProcessor;
import be.tarsos.dsp.io.TarsosDSPAudioFormat;
import be.tarsos.dsp.io.TarsosDSPAudioInputStream;
import be.tarsos.dsp.io.UniversalAudioInputStream;
import be.tarsos.dsp.io.jvm.JVMAudioInputStream;

import javax.imageio.ImageIO;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;

import java.awt.image.BufferedImage;
import java.io.*;

import java.io.File;
import java.io.IOException;
import java.math.RoundingMode;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

//import be.tarsos.dsp.mfcc.MFCC;
import com.jlibrosa.audio.wavFile.WavFile;
import com.jlibrosa.audio.wavFile.WavFileException;
import com.jlibrosa.audio.process.AudioFeatureExtraction;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.imgcodecs.Imgcodecs;
import org.tensorflow.Operand;
import org.tensorflow.op.Scope;
import org.tensorflow.op.audio.Mfcc;

import jm.util.*;
import me.gommeantilegit.sonopy.Sonopy;

import org.opencv.core.Mat;

public class ProjectMain
{
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

    public static void main(String[] args) throws IOException
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
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
        float[] audio = Read.audio("D:/Users/Owen/Final_Year_Project/birdsong/Common_Wood_Pigeon/Common_Wood_Pigeon_0.wav");
        Sonopy sonopy = new Sonopy(44100, 2048, 1024, 2048, 20);
        float[][] mels = sonopy.melSpec(audio);

        double[][] spectrogram = new double[mels.length][mels[0].length];

        for (int i = 0; i < mels.length; i++)
        {
            for (int j = 0; j < mels[0].length; j++)
                spectrogram[i][j] = mels[i][j];
        }

        double[][] power = ProjectMain.powerToDb(spectrogram);

        Mat image = new Mat(power.length, power[0].length, CvType.CV_64FC1);
        for (int row = 0; row < power.length; row++)
        {
            for (int col = 0; col < power[0].length; col++)
            {
                image.put(row, col, power[row][col]);
            }
        }
        Core.normalize(image, image, 0, 255, Core.NORM_MINMAX);
        Imgcodecs.imwrite("temp.jpg", image);

    }
}


import be.tarsos.dsp.AudioDispatcher;
import be.tarsos.dsp.AudioEvent;
import be.tarsos.dsp.AudioProcessor;
import be.tarsos.dsp.io.jvm.AudioDispatcherFactory;
import be.tarsos.dsp.pitch.PitchDetectionHandler;
import be.tarsos.dsp.pitch.PitchDetectionResult;
import be.tarsos.dsp.util.PitchConverter;
import be.tarsos.dsp.util.fft.FFT;

import javax.sound.sampled.UnsupportedAudioFileException;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;


public class MelSpectrogram  implements PitchDetectionHandler {


    private final int bufferSize = 1024 * 4;

    private final int outputFrameWidth = 640*4;
    private final int outputFrameHeight = 480*4;

    String currentPitch = "";
    int position = 0;

    BufferedImage bufferedImage = new BufferedImage(outputFrameWidth,outputFrameHeight, BufferedImage.TYPE_INT_RGB);

    //private PitchProcessor.PitchEstimationAlgorithm algorithm = PitchProcessor.PitchEstimationAlgorithm.YIN;

    AudioProcessor fftProcessor = new AudioProcessor(){

        final FFT fft = new FFT(bufferSize);
        final float[] amplitudes = new float[bufferSize];


        public void processingFinished() {
            // TODO Auto-generated method stub
        }


        public boolean process(AudioEvent audioEvent) {
            float[] audioFloatBuffer = audioEvent.getFloatBuffer();
            float[] transformBuffer = new float[bufferSize * 2];
            System.arraycopy(audioFloatBuffer, 0, transformBuffer, 0, audioFloatBuffer.length);
            fft.forwardTransform(transformBuffer);
            fft.modulus(transformBuffer, amplitudes);
            drawFFT(amplitudes, bufferedImage);
            return true;
        }

    };

    private int frequencyToBin(final double frequency) {
        final double minFrequency = 50; // Hz
        final double maxFrequency = 11000; // Hz
        int bin = 0;
        if (frequency != 0 && frequency > minFrequency && frequency < maxFrequency) {
            double binEstimate;
            final double minCent = PitchConverter.hertzToAbsoluteCent(minFrequency);
            final double maxCent = PitchConverter.hertzToAbsoluteCent(maxFrequency);
            final double absCent = PitchConverter.hertzToAbsoluteCent(frequency * 2);
            binEstimate = (absCent - minCent) / maxCent * outputFrameHeight;
            bin = outputFrameHeight - 1 - (int) binEstimate;
        }
        return bin;
    }

    private void drawFFT(float[] amplitudes, BufferedImage bufferedImage) {


        if(position >= outputFrameWidth){
            return;
        }


        Graphics2D bufferedGraphics = bufferedImage.createGraphics();

        double maxAmplitude=0;
        //for every pixel calculate an amplitude
        float[] pixelAmplitudes = new float[outputFrameHeight];
        //iterate the large array and map to pixels
        for (int i = amplitudes.length/800; i < amplitudes.length; i++) {
            int pixelY = frequencyToBin(i * 44100 / (amplitudes.length * 8));
            pixelAmplitudes[pixelY] += amplitudes[i];
            maxAmplitude = Math.max(pixelAmplitudes[pixelY], maxAmplitude);
        }

        //draw the pixels
        for (int i = 0; i < pixelAmplitudes.length; i++) {
            Color color = Color.black;
            if (maxAmplitude != 0) {

                final int greyValue = (int) (Math.log1p(pixelAmplitudes[i] / maxAmplitude) / Math.log1p(1.0000001) * 255);
                color = new Color(greyValue, greyValue, greyValue);
            }
            bufferedGraphics.setColor(color);
            bufferedGraphics.fillRect(position, i, 3, 1);
        }


        position+=3;
        position = position % outputFrameWidth;
    }


    public BufferedImage convertAudio(File audioFile) throws IOException, UnsupportedAudioFileException
    {
        int overlap = 768 * 4;
        AudioDispatcher dispatcher = AudioDispatcherFactory.fromFile(audioFile, bufferSize, overlap);
        //AudioFormat format = AudioSystem.getAudioFileFormat(audioFile).getFormat();
        //dispatcher.addAudioProcessor(new AudioPlayer(format));

        bufferedImage = new BufferedImage(outputFrameWidth,outputFrameHeight, BufferedImage.TYPE_INT_RGB);

        // add a processor, handle pitch event.
        //dispatcher.addAudioProcessor(new PitchProcessor(algorithm, sampleRate, bufferSize, this));
        dispatcher.addAudioProcessor(fftProcessor);

        position = 0;
        currentPitch = "";

        // run the dispatcher (on a new thread).
        dispatcher.run();

        return bufferedImage;
    }

    public void handlePitch(PitchDetectionResult pitchDetectionResult,AudioEvent audioEvent) {
    }
}
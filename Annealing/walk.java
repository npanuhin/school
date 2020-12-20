import java.util.Scanner;
import java.util.Random;
import java.util.Locale;
import java.lang.Math;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

public class walk {

    static double score(double energy) {
        return 10000 / (energy - 750);
    }

    static double calculate_energy(int[][] mar) {
        double energy = 0;
        for (int i = 1; i < mar.length; ++i) {
            energy += Math.sqrt(
                Math.pow(mar[i - 1][0] - mar[i][0], 2) +
                Math.pow(mar[i - 1][1] - mar[i][1], 2)
            );
        }

        return energy;
    }

    static void write_output(int[][] mar, double energy) {
        try {
            File output_file = new File("output.txt");
            output_file.createNewFile();
            FileOutputStream fileOutputStream = new FileOutputStream(output_file);

            fileOutputStream.write(("Score: " + String.format(Locale.US, "%.2f", score(energy)) + "\n").getBytes());

            for (int i = 0; i < mar.length; ++i) {
                char cs = mar[i][1] > 25 ? (char) ('A' + mar[i][1] - 26) : (char) ('a' + mar[i][1]);
                fileOutputStream.write((cs + "" + (52 - mar[i][0]) + " ").getBytes());
            }
        } catch (IOException e) {
            System.out.println("Output system error");
        }
    }

    public static void main(String[] args) {

        Random random_generator = new Random(System.currentTimeMillis());

        int[][] field = new int[52][52];

        File file = new File("input.txt");
        Scanner vod;
        try {
            vod = new Scanner(file);
        } catch (FileNotFoundException ex) {
            System.out.println("FileNotFoundException");
            return;
        }

        int c = 0;

        double delta, temperature, INITIAL_TEMPERATURE = 0.1;

        for (int i = 0; i < 52; ++i) {
            String sl = vod.nextLine();
            for (int j = 0; j < 52; ++j) {
                if (sl.charAt(j) == '#') {
                    field[i][j] = 1;
                    c++;
                }
            }
        }

        int d = 0;
        int[][] mar = new int[c][2];
        for (int i = 0; i < 52; ++i) {
            for (int j = 0; j < 52; ++j) {
                if (field[i][j] == 1) {
                    mar[d][0] = i;
                    mar[d][1] = j;
                    d++;
                }
            }
        }

        double energy = calculate_energy(mar);

        System.out.printf(
            "Initial energy: %s \tInitial score: %s\n",
            String.format(Locale.US, "%f", energy), String.format(Locale.US, "%.2f", score(energy))
        );

        temperature = INITIAL_TEMPERATURE;

        for (int step = 1; step < 100000000; ++step) {

            int e = random_generator.nextInt(c - 2);
            int f = random_generator.nextInt(c - e - 1) + e + 1;

            delta = 0;
            if (e != 0) {
                delta -= Math.sqrt(
                         Math.pow(mar[e][0] - mar[e - 1][0], 2) +
                         Math.pow(mar[e][1] - mar[e - 1][1], 2)
                );

                delta += Math.sqrt(
                         Math.pow(mar[f][0] - mar[e - 1][0], 2) +
                         Math.pow(mar[f][1] - mar[e - 1][1], 2)
                );
            }

            if (f != c - 1) {
                delta -= Math.sqrt(
                         Math.pow(mar[f + 1][0] - mar[f][0], 2) +
                         Math.pow(mar[f + 1][1] - mar[f][1], 2)
                );

                delta += Math.sqrt(
                         Math.pow(mar[f + 1][0] - mar[e][0], 2) + 
                         Math.pow(mar[f + 1][1] - mar[e][1], 2)
                );
            }

            if (delta < 0 || random_generator.nextDouble() < Math.exp(-delta / temperature)) {
                for (int i = 0; i <= (f - e - 1) / 2; ++i) {
                    int g = mar[e + i][0];
                    int j = mar[e + i][1];
                    mar[e + i][0] = mar[f - i][0];
                    mar[e + i][1] = mar[f - i][1];
                    mar[f - i][0] = g;
                    mar[f - i][1] = j;
                }
            }

            if (step % 10000000 == 0) {
                energy = calculate_energy(mar);

                System.out.printf(
                    "Step: %d \tEnergy: %s \tScore: %s \tTemperature: %s\n",
                    step, String.format(Locale.US, "%f", energy), String.format(Locale.US, "%.2f", score(energy)), String.format(Locale.US, "%f", temperature)
                );

                write_output(mar, energy);
            }

            // temperature = INITIAL_TEMPERATURE / step;
        }

        energy = calculate_energy(mar);

        System.out.printf(
            "Result energy: %s \tResult score: %s",
            String.format(Locale.US, "%f", energy), String.format(Locale.US, "%.2f", score(energy))
        );

        write_output(mar, energy);
    }
}

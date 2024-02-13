import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import sad.project.Consumer;
import sad.project.Message;
import sad.project.Producer;

import java.io.*;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.Function;

public class MessageBrokerTests {
    private static Producer producer;
    private static Consumer consumer;
    private static BufferedWriter writer;
    private static BufferedReader reader;
    private static final String fileName = "subscribe_output";

    @BeforeAll
    public static void init() throws IOException {
        producer = new Producer();
        consumer = new Consumer();
        writer = new BufferedWriter(new FileWriter(fileName));
        reader = new BufferedReader(new FileReader(fileName));
    }

    @AfterAll
    public static void done() throws IOException {
        writer.close();
        reader.close();
    }

    @Test
    public void message_queue_time_guarantee() {
        final Message message1 = Message.builder().key("myKey1").value("myValue1").build();
        final Message message2 = Message.builder().key("myKey2").value("myValue2").build();
        final Message message3 = Message.builder().key("myKey3").value("myValue3").build();

        producer.push(message1);
        producer.push(message2);
        producer.push(message3);

        Assertions.assertEquals(message1.getKey(), consumer.pull().getKey());
        Assertions.assertEquals(message2.getKey(), consumer.pull().getKey());
        Assertions.assertEquals(message3.getKey(), consumer.pull().getKey());
    }

    @Test
    public void subscribe() throws InterruptedException, IOException {
        final Message message1 = Message.builder().key("num1").value("5").build();
        final Message message2 = Message.builder().key("num2").value("7").build();
        final Message message3 = Message.builder().key("num3").value("12").build();
        final Message message4 = Message.builder().key("num4").value("10").build();

        producer.push(message1);
        producer.push(message2);
        producer.push(message3);
        producer.push(message4);

        Function<Message, Void> calculateSquare = (Message message) -> {
            final int square = (int) Math.pow(Integer.parseInt(message.getValue()), 2);
            try {
                writer.write(square + "\n");
            } catch (IOException ignored) {

            }
            return null;
        };

        consumer.subscribe(calculateSquare, 100);
        Thread.sleep(500);
        writer.close();

        final Set<String> expected = Set.of("144", "100", "25", "49");
        Set<String> output = new HashSet<>();

        for (int i = 0; i < 4; i++) {
            output.add(reader.readLine());
        }

        Assertions.assertEquals(expected, output);
    }
}
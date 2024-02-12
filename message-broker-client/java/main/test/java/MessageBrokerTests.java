import org.junit.After;
import org.junit.Before;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import sad.project.Consumer;
import sad.project.Message;
import sad.project.Producer;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.function.Function;

public class MessageBrokerTests {
    private static Producer producer;
    private static Consumer consumer;
    private final ByteArrayOutputStream outContent = new ByteArrayOutputStream();
    private final ByteArrayOutputStream errContent = new ByteArrayOutputStream();
    private final PrintStream originalOut = System.out;
    private final PrintStream originalErr = System.err;

    @Before
    public void setUpStreams() {
        System.setOut(new PrintStream(outContent));
        System.setErr(new PrintStream(errContent));
    }

    @After
    public void restoreStreams() {
        System.setOut(originalOut);
        System.setErr(originalErr);
    }

    @BeforeAll
    public static void init() {
        producer = new Producer();
        consumer = new Consumer();
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
    public void subscribe() {
        final Message message1 = Message.builder().key("num1").value("3").build();
        final Message message2 = Message.builder().key("num2").value("7").build();
        final Message message3 = Message.builder().key("num3").value("12").build();

        producer.push(message1);
        producer.push(message2);
        producer.push(message3);

        Function<Message, Void> calculateSquare = (Message message) -> {
            System.out.println(Math.pow(Integer.getInteger(message.getValue()), 2));
            return null;
        };

        consumer.subscribe(calculateSquare, 1000);

        Assertions.assertEquals("9", outContent.toString());
        Assertions.assertEquals("49", outContent.toString());
        Assertions.assertEquals("144", outContent.toString());
    }
}
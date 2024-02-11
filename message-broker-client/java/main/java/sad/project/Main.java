package sad.project;

import java.util.function.Function;

public class Main {
    public static void main(String[] args) {
        Producer producer = new Producer();

        Consumer consumer = new Consumer();

        producer.push(Message.builder().key("myKey").value("myValue").build());
        producer.push(Message.builder().key("myKey").value("myValue2").build());
        producer.push(Message.builder().key("myKey").value("myValue3").build());

//        final Message pull = consumer.pull();

        Function<Message, Void> printInput = (Message text) -> {
            System.out.println(text);
            return null;
        };

        consumer.subscribe(printInput, 1000);
    }
}

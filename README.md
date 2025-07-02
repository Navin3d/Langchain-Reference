# Langchain-Reference
Simple lanchain chroma db reference

```java
import feign.Feign;
import feign.jackson.JacksonDecoder;
import feign.slf4j.Slf4jLogger;

@Service
public class FeignDynamicPostService {

    private final SubAppConfig subAppConfig;

    public FeignDynamicPostService(SubAppConfig subAppConfig) {
        this.subAppConfig = subAppConfig;
    }

    public List<Post> getAllPosts() {
        List<Post> result = new ArrayList<>();

        Map<String, String> subAppUrls = subAppConfig.getSubAppUrls();
        for (Map.Entry<String, String> entry : subAppUrls.entrySet()) {
            try {
                PostClient client = Feign.builder()
                    .decoder(new JacksonDecoder())
                    .logger(new Slf4jLogger(PostClient.class))
                    .logLevel(feign.Logger.Level.BASIC)
                    .target(PostClient.class, entry.getValue());

                List<Post> posts = client.getPosts();
                result.addAll(posts);
            } catch (Exception e) {
                System.err.println("Failed to fetch from: " + entry.getKey() + " → " + e.getMessage());
            }
        }

        return result;
    }
}
```

```xml
<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-openfeign</artifactId>
		</dependency>
```

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

```java
@Service
public class DynamicPostAggregatorService {

    private final RestTemplate restTemplate;
    private final SubAppConfig subAppConfig;

    public DynamicPostAggregatorService(RestTemplateBuilder builder, SubAppConfig subAppConfig) {
        this.restTemplate = builder.build();
        this.subAppConfig = subAppConfig;
    }

    public List<Post> getAllPosts() {
        List<Post> allPosts = new ArrayList<>();
        Map<String, String> subAppUrls = subAppConfig.getSubAppUrls();

        for (Map.Entry<String, String> entry : subAppUrls.entrySet()) {
            String baseUrl = entry.getValue();
            try {
                ResponseEntity<Post[]> response = restTemplate.getForEntity(baseUrl + "/posts", Post[].class);
                if (response.getStatusCode().is2xxSuccessful()) {
                    allPosts.addAll(Arrays.asList(response.getBody()));
                }
            } catch (Exception e) {
                System.err.println("Error calling " + entry.getKey() + ": " + e.getMessage());
                // Optionally log or track failed services
            }
        }

        return allPosts;
    }
}
```

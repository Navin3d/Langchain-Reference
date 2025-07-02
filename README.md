# Langchain-Reference
Simple lanchain chroma db reference

```java
@Configuration
public class SubAppConfig {

    @Value("${subapps.list}")
    private String subAppList;

    @Autowired
    private Environment env;

    public Map<String, String> getSubAppUrls() {
        Map<String, String> urlMap = new HashMap<>();
        for (String app : subAppList.split(",")) {
            String url = env.getProperty(app + ".url");
            if (url != null) {
                urlMap.put(app, url);
            }
        }
        return urlMap;
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

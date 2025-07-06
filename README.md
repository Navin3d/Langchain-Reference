# Langchain-Reference
Simple lanchain chroma db reference

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("http://localhost:3000")
                .allowedMethods("GET", "POST", "PUT", "DELETE")
                .allowedHeaders("*");
    }
}
```


```java
import feign.Response;
import feign.codec.Decoder;
import feign.FeignException;
import feign.Util;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;

public class JsonThenStringDecoder implements Decoder {

    private final Decoder jsonDecoder;
    private final Decoder stringDecoder;

    public JsonThenStringDecoder(ObjectMapper objectMapper) {
        this.jsonDecoder = new feign.jackson.JacksonDecoder(objectMapper);
        this.stringDecoder = (response, type) -> Util.toString(response.body().asReader(StandardCharsets.UTF_8));
    }

    @Override
    public Object decode(Response response, Type type) throws IOException, FeignException {
        String body = Util.toString(response.body().asReader(StandardCharsets.UTF_8));

        if (body == null || body.trim().isEmpty()) {
            return null;
        }

        // Attempt JSON parse first
        try {
            return jsonDecoder.decode(
                Response.builder()
                        .status(response.status())
                        .headers(response.headers())
                        .reason(response.reason())
                        .request(response.request())
                        .body(body, StandardCharsets.UTF_8)
                        .build(),
                type
            );
        } catch (Exception jsonFail) {
            // Fall back to string (or string[] or whatever is appropriate)
            if (type == String.class) {
                return body;
            } else if (type == String[].class) {
                return new String[] { body };
            } else if (type.getTypeName().contains("List") || type.getTypeName().contains("java.util")) {
                return java.util.Collections.emptyList();
            }

            throw new FeignException.FeignClientException(
                response.status(),
                "Cannot decode as JSON or fallback for type: " + type.getTypeName() + ", response: " + body,
                response.request(),
                response.body().asInputStream()
            );
        }
    }
}

```

```java
@Configuration
public class FeignClientRegistrar {

    @Bean
    public static BeanDefinitionRegistryPostProcessor dynamicFeignClients(SubAppConfig config) {
        return new BeanDefinitionRegistryPostProcessor() {
            @Override
            public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) {
                config.getSubAppUrls().forEach((key, url) -> {
                    String beanName = key + "PostClient";

                    GenericBeanDefinition definition = new GenericBeanDefinition();
                    definition.setBeanClass(PostClient.class);
                    definition.setInstanceSupplier(() -> Feign.builder()
                            .decoder(new JacksonDecoder())
                            .logger(new Slf4jLogger(PostClient.class))
                            .logLevel(feign.Logger.Level.BASIC)
                            .target(PostClient.class, url));
                    registry.registerBeanDefinition(beanName, definition);
                });
            }

            @Override
            public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) {
                // No-op
            }
        };
    }
}
```

```xml
<dependency>
  <groupId>io.github.openfeign</groupId>
  <artifactId>feign-jackson</artifactId>
  <version>12.4</version> <!-- or latest -->
</dependency>


<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-openfeign</artifactId>
		</dependency>
```

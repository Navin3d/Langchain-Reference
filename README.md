# Langchain-Reference
Simple lanchain chroma db reference

deleteCookie(name: string) {
  document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}


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
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

import javax.net.ssl.SSLContext;
import java.io.FileInputStream;
import java.security.KeyStore;

import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.ssl.SSLContexts;

@Configuration
public class SslRestTemplateConfig {

    @Bean
    public RestTemplate restTemplate() throws Exception {
        // Load the truststore
        KeyStore trustStore = KeyStore.getInstance("PKCS12");
        FileInputStream trustStoreStream = new FileInputStream("src/main/resources/my-truststore.p12");
        trustStore.load(trustStoreStream, "changeit".toCharArray());

        // Create SSL context
        SSLContext sslContext = SSLContexts.custom()
                .loadTrustMaterial(trustStore, null) // No need for password if just trusting
                .build();

        // Create socket factory with the SSL context
        SSLConnectionSocketFactory socketFactory =
                new SSLConnectionSocketFactory(sslContext);

        // Create HttpClient with custom SSL config
        CloseableHttpClient httpClient = HttpClients.custom()
                .setSSLSocketFactory(socketFactory)
                .build();

        // Create request factory with custom HttpClient
        HttpComponentsClientHttpRequestFactory factory =
                new HttpComponentsClientHttpRequestFactory(httpClient);

        return new RestTemplate(factory);
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

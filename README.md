# Langchain-Reference
Simple lanchain chroma db reference

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
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-openfeign</artifactId>
		</dependency>
```

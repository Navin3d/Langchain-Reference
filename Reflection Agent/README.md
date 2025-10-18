# Basic Reflection Agent
- [Excali Draw](https://excalidraw.com/) Used to Convert mermaid diagram to graph.
- [Cource Reference](https://github.com/emarco177/langgraph-course/tree/project/reflection-agent)


```mermaid
graph TD;
	__start__([<p>__start__</p>]):::first
	generate(generate)
	reflect(reflect)
	__end__([<p>__end__</p>]):::last
	__start__ --> generate;
	generate -.-> __end__;
	generate -.-> reflect;
	reflect --> generate;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
```

![img.png](img.png)

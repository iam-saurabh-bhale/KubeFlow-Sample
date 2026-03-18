from kfp import dsl
from kfp import compiler

# Define a simple component
@dsl.component(base_image="python:3.9-slim")
def say_hello(name: str) -> str:
    """A simple component that says hello to a given name."""
    hello_text = f'Hello, {name}!'
    print(hello_text)
    return hello_text

# Define pipeline
@dsl.pipeline(
    name="hello-world-pipeline",
    description="A basic pipeline that prints a greeting."
)
def hello_pipeline(recipient: str = "World"):
    """This pipeline runs the say_hello component."""
    say_hello(name=recipient)

if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=hello_pipeline,
        package_path='hello_world_pipeline.yaml'
    )

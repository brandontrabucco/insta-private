# InSTA: Towards Internet-Scale Training For Agents

![Pipeline Overview](https://data-for-agents.github.io/static/images/pipeline_overview.png)

**Brandon Trabucco (1) Gunnar Sigurdsson (2) Robinson Piramuthu (2) Ruslan Salakhutdinov (1)**

**(1) Carnegie Mellon University, Machine Learning Department (2) Amazon**

The predominant approach for training web navigation agents gathers human demonstrations for a set of popular websites and hand-written tasks, but it is becoming clear that human data are an inefficient resource. We develop a pipeline to facilitate Internet-scale training for agents without laborious human annotations. In the first stage, an LLM generates tasks for 150k diverse websites. In the next stage, LLM agents complete tasks and produce trajectories. In the final stage, an LLM reviews the trajectories and judges their success. Language models are competitive with human annotators, detecting and filtering out harmful content with an accuracy of 97%, generating feasible tasks with an 89% rate, and judging successful trajectories with an 82.6% accuracy. Scaling the pipeline, agents based on Llama 3.1 70B solve 16.7% of tasks for 150k sites. Training on the data generated by our pipeline is competitive with training on human demonstrations. In data-limited settings derived from Mind2Web and WebLINX, we improve Step Accuracy by up to +89.5% and +122.1% respectively for agents trained on mixtures of data from our pipeline, and human data. When training agents with all available human data from these benchmarks, agents fail to generalize to diverse real sites, and adding our data improves their generalization by +149.0% for WebLINX and +156.3% for Mind2Web. Code available at: [data-for-agents.github.io](https://data-for-agents.github.io).

[website](https://data-for-agents.github.io)    |    [paper](https://arxiv.org/abs/2502.06776)    |    [data](https://huggingface.co/datasets/data-for-agents/insta-150k)

## Official Gym Environment & LLM Tools

We are excited to present the **official Gym Environment and LLM Tools** for *InSTA: Towards Internet-Scale Training For Agents (https://arxiv.org/abs/2502.06776)*. Our guide below will help you get started with our pipeline in < 5 minutes.

```bash
pip install git+https://github.com/data-for-agents/insta
```

We provide an official `gym.Env` environment for LLM training, and official tools for popular LLM inference frameworks, including `transformers.agents.tools`, and `langchain.tools`. See the quickstart guide below, and start by loading one of our tools.

## Loading The Demo Tool

We provide a gradio demo at `http://insta.btrabuc.co:7860` for the demo tool below that allows you to start using our tools immediately after installing the `insta` package using pip. Use the demo tool respectfully, the instance serving it is relatively modest.

```python
from insta import InstaTransformersGradioTool

tool = InstaTransformersGradioTool()

outputs = tool(
    url = "http://google.com"
)
```

Running the above will produce the following observation:

```
Here is your assigned session ID: `awesome-avocado`

You are visiting the URL: `http://google.com`

Here is the current viewport rendered in markdown:

Google [id: 4] About link [id: 5] Store link [id: 11] Gmail link [id: 13] Search for Images link [id: 16] Google apps link [id: 21] Sign in link Google image 
## Search Form
[id: 77] """

""" (q textbox)
[id: 89] Search by voice button
[id: 96] Search by image button
[id: 238] "Google Search" (btnK submit input)
[id: 239] "I'm Feeling Lucky" (btnI submit input) [id: 285] Advertising link [id: 286] Business link [id: 287] How Search works link [id: 289] data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAYCAMAAAAiV0... link [id: 293] Privacy link [id: 294] Terms link [id: 300] Settings button
```

InSTA produces a compact markdown representation of webpages. We can represent typical webpages in as few as ~200 tokens (the demo above requires just 240 tokens). The `InstaTransformersGradioTool` uses javascript-based actions by default, and we can fill the textbox marked `[id: 77]` with the following action. The action format can be overridden to a JSON-based format, and custom formats depending on your needs.

```python
outputs = tool(
    session_id = "awesome-avocado",
    action = "page.locator(\"[id='77']\").fill(\"latest meta llama models\")"
)
```

For LLM tools, frameworks like Langchain and Transformers assume they are stateless, so the session ID assigned by the tool must be propagated to future calls (note the `session_id = "awesome-avocado"` above). Running this action produces the following observation:

```
Here is your assigned session ID: `awesome-avocado`

You are visiting the URL: `http://google.com`

Here is the current viewport rendered in markdown:

Google [id: 4] About link [id: 5] Store link [id: 11] Gmail link [id: 13] Search for Images link [id: 16] Google apps link [id: 21] Sign in link Google image 
## Search Form
[id: 77] """
latest meta llama models
""" (q textbox)
[id: 83] Clear button
[id: 89] Search by voice button
[id: 96] Search by image button

* latest meta llama **model**
* llama **model** meta
* llama meta **demo**

[id: 325] "Google Search" (btnK submit input)
[id: 326] "I'm Feeling Lucky" (btnI submit input)
[id: 329] Report inappropriate predictions button
[id: 333] "Google Search" (btnK submit input)
[id: 334] "I'm Feeling Lucky" (btnI submit input) [id: 380] Advertising link [id: 381] Business link [id: 382] How Search works link [id: 384] data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAYCAMAAAAiV0... link [id: 388] Privacy link [id: 389] Terms link [id: 395] Settings button
```

InSTA captures the structure, flow, hierarchy, and style of the webpage in its markdown representation. Interactive elements, including forms, buttons, links, and other widgets are noted with an `[id: ##]` identifier for agents.

## Serving The Environment Locally

The previous demo connects to an environment served at `http://insta.btrabuc.co:7860`, which should be used respectfully. To serve the environment locally, we provide a docker container. [Install docker](https://docs.docker.com/engine/install/), and run the following commands in your terminal:

```bash
docker pull brandontrabucco/insta-browser-environment
docker run -p 7860:7860 -p 3000-3007:3000-3007 -t brandontrabucco/insta-browser-environment
```

This will serve the gradio demo (located at `gradio/app.py`) on your machine at `http://localhost:7860`. Once the environment is running, you can connect to it from the official tools, for example:

```python
from insta import (
    InstaTool
)

tool = InstaTool()

outputs = tool(
    url = "http://btrabuc.co"
)
```

The base `InstaTool` tool is a `Callable` that accepts a `session_id` argument, `url` argument, and an `action` argument. Interact with the `InstaTool` using the following workflow:

1) Submit a `url` to start a new browsing session.
2) Copy the assigned `session_id`, and submit an `action`.

The base `InstaTool` tool returns an instance of `InstaToolOutput` with a `session_id` key, a `processed_text` key, and a `screenshot` key. When building custom tools on top of InSTA, process these into your own tailored LLM prompt.

## Loading The Gym Environment

To facilitate training LLM agents using InSTA, we provide an **official Gym environment**. After pulling our docker image, and starting the environment following the last section, you can load the InSTA Gym environment as follows:

```python
from insta import InstaEnv

env = InstaEnv()

obs, info = env.reset(url = "http://example.com")
```

The environment expects actions in the form of a `BrowserAction` instance. This action represents a chain of function calls in the Playwright API, and can be parsed from LLM-generated texted using an `ActionParser`.

~~~python
from insta import ACTION_PARSERS

action_parser = ACTION_PARSERS["javascript"]()

action = action_parser.parse_action("""

Here is my action:

```javascript
page.locator("[id='5']").click()
```

""")

obs, reward, done, truncated, info = obs.step(action)

~~~

## Citing Us

Please cite our work using the following bibtex:

```
@misc{Trabucco2025InSTA,
  title={InSTA: Towards Internet-Scale Training For Agents},
  author={Brandon Trabucco and Gunnar Sigurdsson and Robinson Piramuthu and Ruslan Salakhutdinov},
  year={2025},
  eprint={2502.06776},
  archivePrefix={arXiv},
  primaryClass={cs.LG},
}
```
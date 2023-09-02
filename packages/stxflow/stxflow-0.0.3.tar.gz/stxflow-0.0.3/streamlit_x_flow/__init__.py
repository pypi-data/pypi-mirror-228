import os
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True
# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("streamlit_x_flow"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "streamlit_x_flow",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:8322",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_x_flow", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def streamlit_x_flow(schema, job_params, key=None):
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(schema=schema, job_params=job_params, key=key, default=0)

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run streamlit_x_flow/__init__.py`
if not _RELEASE:
    import streamlit as st
    # Create a second instance of our component whose `name` arg will vary
    # based on a text_input widget.
    #
    # We use the special "key" argument to assign a fixed identity to this
    # component instance. By default, when a component's arguments change,
    # it is considered a new instance and will be re-mounted on the frontend
    # and lose its current state. In this case, we want to vary the component's
    # "name" argument without having it get recreated.

    schema = dict({
            'nodes': [
                {
                    'id': 'node1',
                    'renderKey': 'DND_NDOE',
                    'width': 180,
                    'height': 36,
                    'label': '训练',
                    'ports': [
                        {
                            'id': 'node1-output-1',
                            'type': 'output',
                            'group': 'bottom',
                            'tooltip': '输出桩'
                        }
                    ],
                    '_order': 0
                },
                {
                    'id': 'node2',
                    'renderKey': 'DND_NDOE',
                    'width': 180,
                    'height': 36,
                    'label': '评估',
                    'ports': [
                        {
                            'id': 'node2-input-1',
                            'type': 'input',
                            'group': 'top',
                            'tooltip': '输入桩',
                            'connected': True
                        },
                        {
                            'id': 'node2-output-1',
                            'type': 'output',
                            'group': 'bottom',
                            'tooltip': '输出桩'
                        }
                    ],
                    '_order': 0
                },
                {
                    'id': 'node3',
                    'renderKey': 'DND_NDOE',
                    'width': 180,
                    'height': 36,
                    'label': '发布',
                    'ports': [
                        {
                            'id': 'node3-input-1',
                            'type': 'input',
                            'group': 'top',
                            'tooltip': '输入桩',
                            'connected': True
                        }
                    ],
                    'x': 300,
                    'y': 180,
                    '_order': 1
                }
            ],
            'edges': [
                {
                    'id': '0db5dfc5-b5a6-4f29-b245-4ecbfb16bc50',
                    'source': 'node1',
                    'target': 'node2',
                    'sourcePortId': 'node1-output-1',
                    'targetPortId': 'node2-input-1',
                    'connector': {
                        'name': 'rounded'
                    },
                    'router': {
                        'name': 'manhattan'
                    }
                },
                {
                    'id': 'e6d27e39-8ce0-4eeb-8127-9f8c23bed0ca',
                    'source': 'node2',
                    'target': 'node3',
                    'sourcePortId': 'node1-output-1',
                    'targetPortId': 'node3-input-1',
                    'connector': {
                        'name': 'rounded'
                    },
                    'router': {
                        'name': 'manhattan'
                    }
                }
            ]
        })
    pipeline_Params = streamlit_x_flow(schema, job_params=dict({"panel": "preview"}), key="foo")


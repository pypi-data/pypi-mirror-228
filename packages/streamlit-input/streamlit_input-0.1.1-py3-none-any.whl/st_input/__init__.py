from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple
import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called st_input,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"st_input", path=str(frontend_dir)
)

def st_input(
    label: str,
    value: str = "",
    max_chars: Optional[int] = None,
    key: Optional[str] = None,
    type: str = "text",
    on_change: Optional[Callable] = None,
    args: Optional[Tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    *,
    placeholder: Optional[str]= None,
    disabled: bool = False,
    label_visibility: str = "visible",
) -> str:
        
        r"""Display a single-line text input widget.

        Parameters
        ----------
        label : str
            A short label explaining to the user what this input is for.
        value : object
            The text value of this widget when it first renders. This will be
            cast to str internally.
        max_chars : int or None
            Max number of characters allowed in text input.
        key : str or int
            An optional string or integer to use as the unique key for the widget.
            If this is omitted, a key will be generated for the widget
            based on its content. Multiple widgets of the same type may
            not share the same key.
        type : str
            The type of the text input. This can be any valid html inpute type
            such as "phone", "password", "email", or anything. By default it is
            "text", Note for "phone" it will set the input type as "tel".
        on_change : callable
            An optional callback invoked when this text input's value changes.
        args : tuple
            An optional tuple of args to pass to the callback.
        kwargs : dict
            An optional dict of kwargs to pass to the callback.
        placeholder : str or None
            An optional string displayed when the text input is empty. If None,
            no text is displayed. This argument can only be supplied by keyword.
        disabled : bool
            An optional boolean, which disables the text input if set to True.
            The default is False. This argument can only be supplied by keyword.
        label_visibility : "visible", "hidden", or "collapsed"
            The visibility of the label. If "hidden", the label doesn't show but there
            is still empty space for it above the widget (equivalent to label="").
            If "collapsed", both the label and the space are removed. Default is
            "visible". This argument can only be supplied by keyword.

        Returns
        -------
        str
            The current value of the text input widget.
"""   
        if key is None:
            key = "st_input" + label

        component_value = _component_func(
            label=label,
            value=value,
            key=key,
            default=value,
            max_chars=max_chars,
            type=type,
            placeholder=placeholder,
            disabled=disabled,
            label_visibility=label_visibility,
        )
        if on_change is not None:
            if "__previous_values__" not in st.session_state:
                st.session_state["__previous_values__"] = {}

            if component_value != st.session_state["__previous_values__"].get(key, value):
                st.session_state["__previous_values__"][key] = component_value

                if on_change:
                    if args is None:
                        args = ()
                    if kwargs is None:
                        kwargs = {}
                    on_change(*args, **kwargs)

        return component_value

def main():
    from datetime import datetime

    st.write("## Default input")
    value = st_input("Enter a value")
    st.write(value)

    "## st_input with hidden label"
    value = st_input("You can't see this", label_visibility="hidden")
    st.write(value)
    

    "## st_input with collapsed label"
    value = st_input("This either", label_visibility="collapsed")
    st.write(value)
    "## st_inputmax_chars 5"
    value = st_input("st_inputmax chars", max_chars=5)
    st.write(value)

    "## st_input with password type"
    value = st_input("Password", value="Hello World", type="password")
    st.write(value)

    "## st_input with disabled"
    value = st_input("Disabled", value="Hello World", disabled=True)
    st.write(value)

    "## st_input with default value"
    value = st_input("Default value", value="Hello World")
    st.write(value)

    "## st_input with placeholder"
    value = st_input("Has placeholder", placeholder="A placeholder")
    st.write(value)

    def on_change():
        st.write("Value changed!", datetime.now())

    def on_change2(*args, **kwargs):
        st.write("Value changed!", args, kwargs)

    "## st_input with on_change callback"
    value = st_input("Has an on_change", on_change=on_change)

    st.write(value)

    "## st_input with args"
    value = st_input(
        "Enter a fourth value...",
        on_change=on_change2,
        args=("Hello", "World"),
        kwargs={"foo": "bar"},
    )
    st.write(value)

    "## Standard text input for comparison"
    value = st.text_input("Enter a value")

    st.write(value)

    st.write(st.session_state)

    


if __name__ == "__main__":
    main()

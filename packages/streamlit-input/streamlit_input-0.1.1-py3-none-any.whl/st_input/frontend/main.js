// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  // Only run the render code the first time the component is loaded.
  if (!window.rendered) {
    const {
      label,
      value,
      max_chars,
      type,
      placeholder,
      disabled,
      label_visibility,
    } = event.detail.args;

    const text_input = document.getElementById('text_input')
    const label_el = document.getElementById('label')
    const root = document.getElementById("root")

    if(value && !text_input.value){
      text_input.value = value
    }

    if (label_el) {
      label_el.innerText = label
    }
    text_input.innerText = label

    if(type == "password"){
      text_input.type = "password"
    }
    else if (type == "phone" || type == "tel") {
      text_input.type = "tel"
    }
    else if (type == "email"){
      text_input.type = "email"
    }
    else if (type =="number"){
      text_input.type = "number"
    }else{
      text_input.type = type
    }

    if (max_chars){
      text_input.maxLength = max_chars
    }

    if (placeholder){
      text_input.placeholder = placeholder
    }

    if (disabled){
      text_input.disabled = true
      label_el.disabled = true
      root.classList.add("disabled")
    }
    if (label_visibility == "hidden") {
      root.classList.add("label-hidden")
    }else if (label_visibility == "collapsed") {
      root.classList.add("label-collapsed")
      Streamlit.setFrameHeight(45)
    }
    
    text_input.onchange = function() {
      var inputValue = text_input.value
      console.log(inputValue)
      sendValue(inputValue)
    }  
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(70)

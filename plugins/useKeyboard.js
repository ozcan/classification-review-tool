window.hyperdiv.registerPlugin("useKeyboard", (ctx) => {
  if (window._KEYBOARD_PLUGIN_INSTALLED === undefined) {
    document.addEventListener("keydown", (event) => {
      event.preventDefault();
      ctx.updateProp("keyName", event.key);
    });
    document.addEventListener("keyup", (event) => {
      event.preventDefault();
      ctx.updateProp("keyName", "");
    });
    window._KEYBOARD_PLUGIN_INSTALLED = true;
  }
});

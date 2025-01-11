module.exports = {
  content: [
    "./templates/**/*.html",        // Flask templates
    "./static/src/**/*.js",         // Any JS files
    "./node_modules/flowbite/**/*.js", // Flowbite components
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')      // Include Flowbite plugin
  ],
};

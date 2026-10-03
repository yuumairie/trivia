// NOTE: this plugin file is not currently imported anywhere (main.ts
// doesn't register it), so it has no effect on the running app -- it's
// leftover scaffolding from `vue-cli-plugin-bootstrap-vue`. Left here,
// updated to the Vue 3 / bootstrap-vue-next API, in case it's wired up
// later; the old `import Vue from 'vue'; Vue.use(...)` pattern doesn't
// exist in Vue 3 (no default-exported global constructor).
import { createBootstrap } from 'bootstrap-vue-next/plugins/createBootstrap';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css';

export default createBootstrap();

import { createApp } from 'vue';
import {createPinia} from 'pinia';
import 'bootstrap/dist/css/bootstrap.css';
import App from './App.vue';
(window as any)._galaxyInstance={config:{enable_tool_recommendations:false},root:'/',user:{get:()=>null}};
createApp(App).use(createPinia()).directive('g-tooltip',{}).mount('#app');

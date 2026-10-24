import base from './vite.config.mjs';
const config=base({command:'serve',mode:'development'});
export default {...config,plugins:config.plugins.filter(p=>!p.name?.includes('dev-server')),server:{host:'127.0.0.1',port:5178,strictPort:true}};

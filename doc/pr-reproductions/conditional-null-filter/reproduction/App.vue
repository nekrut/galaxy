<script setup lang="ts">
import {computed,provide,ref,onMounted} from 'vue';
import {zoomIdentity} from 'd3-zoom';
import {useWorkflowStores} from '@/composables/workflowStores';
import {DatatypesMapperModel} from '@/components/Datatypes/model';
import {terminalFactory} from '@/components/Workflow/Editor/modules/terminals';
import {getCombinedStepInputs} from '@/stores/workflowStepStore';
import {mockOffset} from '@/components/Workflow/Editor/test_fixtures';
import Node from '@/components/Workflow/Editor/Node.vue';
import SVGConnection from '@/components/Workflow/Editor/SVGConnection.vue';
import datatypes from './datatypes.json';
import steps from './steps.json';
provide('workflowId','conditional-collection-reproduction');
provide('transform',ref(zoomIdentity));provide('isDragging',ref(false));
const stores=useWorkflowStores('conditional-collection-reproduction');
const mapper=new DatatypesMapperModel(datatypes);
for(const step of steps) stores.stepStore.addStep(step as any);
for(let pass=0;pass<3;pass++) for(const step of Object.values(stores.stepStore.steps)) {
 for(const source of [...getCombinedStepInputs(step,stores.stepStore),...step.outputs]) terminalFactory(step.id,source,mapper,stores).getInvalidConnectedTerminals();
}
const invalid=computed(()=>Object.entries(stores.connectionStore.invalidConnections));
const phase=new URLSearchParams(window.location.search).get('phase') || 'Reproduction';
const scroll={left:0,top:0,x:ref(0),y:ref(0),isScrolling:ref(false),arrivedState:{left:true,right:true,top:true,bottom:true},directions:{left:false,right:false,top:false,bottom:false}};
onMounted(()=>{(window as any).repro={invalid:stores.connectionStore.invalidConnections,connections:stores.connectionStore.connections.length};});
</script>
<template>
 <main>
  <header><div class="brand">Galaxy workflow editor · local reproduction</div><h1>{{phase}}: conditional merge → Filter null elements</h1><p>ATAC-seq collection types and tool interfaces from usegalaxy.org; upstream grouping represented by collection inputs.</p></header>
  <section class="result" :class="invalid.length?'failure':'success'" data-testid="result">
   <strong>{{invalid.length}} invalid connections</strong>
   <span v-if="invalid.length">{{invalid[0]?.[1]}}</span>
   <span v-else>Both null-filter inputs accept the existing collections. Optional elements remain marked as optional.</span>
  </section>
  <section class="canvas">
   <svg width="1190" height="590"><SVGConnection v-for="(connection,i) in stores.connectionStore.connections" :key="i" :id="'connection-'+i" :connection="connection" /></svg>
   <Node v-for="step in Object.values(stores.stepStore.steps)" :key="step.id" :id="step.id" :step="step" :name="step.name" :content-id="step.content_id" :active-node-id="null" :datatypes-mapper="mapper" :root-offset="mockOffset" :scroll="scroll as any" :readonly="true" />
  </section>
  <footer><strong>Execution condition:</strong> merge only when <code>inputs.bams.length &gt; 1</code>.<br/>Skipped groups become null elements inside an existing collection. The two filters remove those null elements.</footer>
 </main>
</template>
<style>
body{margin:0;background:#f2f5f8;color:#23384d;font-family:Arial,sans-serif}main{width:1230px;margin:20px auto;background:white;border:1px solid #d6dfe8;border-radius:8px;overflow:hidden}header{padding:22px 25px 12px;background:#263c53;color:white}.brand{font-size:14px;color:#bdcfe2;font-weight:600;margin-bottom:10px}h1{font-size:25px;margin:0 0 10px}header p{font-size:14px;margin:0}.result{margin:18px 20px 0;padding:13px 16px;border-radius:5px;border:1px solid;display:flex;gap:20px;font-size:14px}.failure{background:#fff1f2;border-color:#d9534f;color:#9c2530}.success{background:#edf9f0;border-color:#4d9563;color:#215e33}.canvas{position:relative;margin:0 20px;width:1190px;height:590px;background:radial-gradient(#dce3e9 1px, transparent 1px);background-size:16px 16px}.canvas svg{position:absolute;inset:0}.workflow-node{font-size:14px}.node-title{font-weight:600}.card-header{background:#e9eff5}footer{background:#f5f8fa;padding:16px 25px;line-height:1.7;font-size:14px;border-top:1px solid #dde4eb}
</style>

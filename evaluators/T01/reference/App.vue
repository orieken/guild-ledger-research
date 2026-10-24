<script setup lang="ts">
import { onMounted, ref } from 'vue'
type Quest = {id:string; title:string; description:string; difficulty:string; status:string; min_party_size:number; max_party_size:number; min_level:number; reward_gold:number}
const q=ref(''), difficulty=ref(''), status=ref(''), quests=ref<Quest[]>([]), detail=ref<Quest|null>(null)
const loading=ref(false), error=ref(''), empty=ref(false)
let listVersion=0, detailVersion=0
async function load() {
  const version=++listVersion
  loading.value=true;error.value='';empty.value=false
  const params=new URLSearchParams()
  if(q.value)params.set('q',q.value)
  if(difficulty.value)params.set('difficulty',difficulty.value)
  if(status.value)params.set('status',status.value)
  try {
    const response=await fetch('/api/quests?'+params.toString())
    if(!response.ok)throw new Error('List failed')
    const body=await response.json()
    if(version!==listVersion)return
    quests.value=body.quests;empty.value=quests.value.length===0
  } catch {
    if(version===listVersion)error.value='Could not load quests. Please try again.'
  } finally {
    if(version===listVersion)loading.value=false
  }
}
async function open(id:string) {
  const version=++detailVersion
  error.value=''
  try {
    const response=await fetch('/api/quests/'+encodeURIComponent(id))
    if(!response.ok)throw new Error('Detail failed')
    const body=await response.json()
    if(version!==detailVersion)return
    detail.value=body
  } catch {
    if(version===detailVersion)error.value='Could not load quest details.'
  }
}
onMounted(load)
</script>
<template>
  <main>
    <h1>Guild Ledger</h1>
    <form @submit.prevent="load">
      <label>Search <input v-model="q" type="search"></label>
      <label>Difficulty <select v-model="difficulty"><option value="">All</option><option value="easy">Easy</option><option value="medium">Medium</option><option value="hard">Hard</option></select></label>
      <label>Status <select v-model="status"><option value="">All</option><option value="open">Open</option><option value="closed">Closed</option></select></label>
      <button type="submit">Apply</button>
    </form>
    <p v-if="loading" role="status">Loading quests…</p>
    <p v-else-if="empty" role="status">No quests match these filters.</p>
    <p v-if="error" role="alert">{{error}}</p>
    <ul><li v-for="quest in quests" :key="quest.id">{{quest.title}} <button @click="open(quest.id)">View {{quest.title}}</button></li></ul>
    <section v-if="detail" aria-label="Quest details">
      <h2>{{detail.title}}</h2><p>{{detail.description}}</p>
      <dl>
        <dt>Difficulty</dt><dd>{{detail.difficulty}}</dd>
        <dt>Status</dt><dd>{{detail.status}}</dd>
        <dt>Minimum party size</dt><dd>{{detail.min_party_size}}</dd>
        <dt>Maximum party size</dt><dd>{{detail.max_party_size}}</dd>
        <dt>Minimum level</dt><dd>{{detail.min_level}}</dd>
        <dt>Reward gold</dt><dd>{{detail.reward_gold}}</dd>
      </dl>
    </section>
  </main>
</template>

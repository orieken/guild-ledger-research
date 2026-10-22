<script setup lang="ts">
import { ref, onMounted } from 'vue'
type Quest = {id:string;title:string;description:string}
const quests=ref<Quest[]>([]), detail=ref<Quest|null>(null), error=ref('')
onMounted(async()=>{try { const r=await fetch('/api/quests'); if(!r.ok) throw new Error('request'); quests.value=(await r.json()).quests } catch {error.value='Could not load quests'} })
async function open(id:string) {try {const r=await fetch('/api/quests/'+encodeURIComponent(id));if(!r.ok) throw new Error('request');detail.value=await r.json()}catch{error.value='Could not load quest'}}
</script>
<template><main><h1>Guild Ledger</h1><p v-if="error" role="alert">{{error}}</p><ul><li v-for="q in quests" :key="q.id">{{q.title}} <button @click="open(q.id)">View {{q.title}}</button></li></ul><p v-if="detail">{{detail.description}}</p></main></template>

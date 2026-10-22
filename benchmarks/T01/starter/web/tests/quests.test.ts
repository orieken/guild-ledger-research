import { render, screen, fireEvent } from '@testing-library/vue'
import { expect, test, vi } from 'vitest'
import App from '../src/App.vue'
const quest = {id:'q-ash',title:'Ash Orchard',description:'Recover the orchard bells.',difficulty:'easy',status:'open',min_party_size:1,max_party_size:4,min_level:1,reward_gold:30}
test('browse a quest and open its details', async () => {
 vi.stubGlobal('fetch',vi.fn(async (input: string | URL | Request) => new Response(JSON.stringify(String(input).split('?')[0].endsWith('/q-ash') ? quest : {quests:[quest]}),{status:200,headers:{'Content-Type':'application/json'}})))
 render(App)
 const open = await screen.findByRole('button',{name:'View Ash Orchard'})
 await fireEvent.click(open)
 expect(await screen.findByText('Recover the orchard bells.')).toBeVisible()
})
test('a failed list request produces accessible feedback', async () => {
 vi.stubGlobal('fetch',vi.fn(async () => { throw new Error('offline') }))
 render(App)
 expect(await screen.findByRole('alert')).toHaveTextContent(/.+/)
})

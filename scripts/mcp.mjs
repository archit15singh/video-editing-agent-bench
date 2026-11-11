import fs from 'node:fs';
import path from 'node:path';
import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
const root=path.resolve(import.meta.dirname,'..');
const adapter=process.argv[2];
const plan=process.argv[3]?JSON.parse(fs.readFileSync(process.argv[3],'utf8')):[];
const dir=path.join(root,'results',adapter);fs.mkdirSync(dir,{recursive:true});
const baseEnv={PATH:`${root}/.tools/bin:/opt/homebrew/bin:${process.env.PATH}`,TMPDIR:process.env.TMPDIR??'/tmp',LANG:'en_US.UTF-8'};
const env=adapter==='nodetool'?{...baseEnv,XDG_DATA_HOME:`${root}/.cache/nodetool-data`,XDG_CACHE_HOME:`${root}/.cache`,NODETOOL_WORKSPACES_DIR:`${root}/results/nodetool/media/workspaces`,PORT:'17777'}:{...baseEnv,MAKEMYCLIP_WORKSPACE:`${root}/results/makemyclip/media`,MAKEMYCLIP_WHISPER_MODEL:`${root}/.tools/models/ggml-base.en.bin`,MAKEMYCLIP_WHISPER_PATH:`${root}/.tools/whisper.cpp/build/bin/whisper-cli`};
const executable=adapter==='nodetool'?'adapters/nodetool/node_modules/.bin/nodetool-mcp':'node_modules/.bin/clip';
const args=adapter==='nodetool'?['serve']:['mcp'];
const stderr=fs.createWriteStream(path.join(dir,'mcp-stderr.log'),{flags:'a'});
const transport=new StdioClientTransport({command:path.join(root,executable),args,env,cwd:root,stderr:'pipe'});
transport.stderr?.pipe(stderr);
const client=new Client({name:'video-agent-benchmark',version:'0.1.0'});
let log=[];
try{
 const start=performance.now();await client.connect(transport);
 const listed=await client.listTools();fs.writeFileSync(path.join(dir,'tools.json'),JSON.stringify(listed,null,2));
 console.log(`Connected ${adapter}: ${listed.tools.length} tools in ${((performance.now()-start)/1000).toFixed(2)}s`);
 for(let i=0;i<plan.length;i++){
   const action=plan[i],t=performance.now();
   const result=await client.callTool(action,undefined,{timeout:300000});
   log.push({action,result,seconds:(performance.now()-t)/1000});
   fs.writeFileSync(path.join(dir,`mcp-run-${path.basename(process.argv[3],'.json')}.json`),JSON.stringify(log,null,2));
   console.log(JSON.stringify(result, (key,value)=>key==='data'&&typeof value==='string'&&value.length>1000?'[binary image omitted]':value).slice(0,4000));
   for(const block of result.content??[]){if(block.type==='text'){try{const inner=JSON.parse(block.text);if(inner.ok===false)throw new Error(inner.error??'Nested tool failure');}catch(error){if(!(error instanceof SyntaxError))throw error;}}}
   if(result.isError)throw new Error(`Tool failed: ${action.name}`);
 }
}catch(error){console.error(error);process.exitCode=1;}
finally{await client.close();stderr.end();}

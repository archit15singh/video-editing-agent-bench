import React from 'react';
import {AbsoluteFill,Composition,Sequence,OffthreadVideo,Img,registerRoot,staticFile,useCurrentFrame,interpolate} from 'remotion';
import config from '../../fixtures/round-two/composition.json';
const inout=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const ease=t=>1-Math.pow(1-t,3);
function Plate({index,version,accent}){
 const f=useCurrentFrame(),t=f/30;
 const p=Math.min(1,t/.5),label=Math.min(1,Math.max(0,(t-.2)/.4));
 return <div style={{position:'absolute',left:425,top:145,width:800,height:450,background:'#0d161c'}}>
  <div style={{position:'absolute',inset:0,transform:`translateX(${index===1?-16*inout(Math.max(0,Math.min(1,(t-1.5)/2))):0}px) scale(${.94+.06*ease(p)+(index===1?.04*inout(Math.max(0,Math.min(1,(t-1.5)/2))):0)})`,opacity:p}}><Img src={staticFile(`${version}-screen-${index}.png`)} style={{width:800,height:467,border:'1px solid #34434a',borderRadius:12}}/><div style={{position:'absolute',left:158,top:162,width:580,height:55,border:`3px solid ${accent}`,borderRadius:8,transform:`translateY(${index===0?66*inout(Math.max(0,Math.min(1,(t-2)/.4)))+67*inout(Math.max(0,Math.min(1,(t-3.5)/.4))):0}px)`,opacity:Math.max(0,Math.min(1,(t-.5)/.4))}}/></div>
  <div style={{position:'absolute',left:0,top:-45,font:'24px R2Serif',color:accent,opacity:label,transform:`translateY(${20*(1-ease(label))}px)`}}>0{index+1} / {config.titles[index]}</div>
  <div style={{position:'absolute',left:162,top:370,display:'flex',gap:12}}>{[90,150,210].map((w,i)=><div key={w} style={{width:w,height:8,background:accent,transformOrigin:'left',transform:`scaleX(${1-Math.pow(1-Math.max(0,Math.min(1,(t-1-i*.2)/.8)),3)})`}}/>)}</div>
 </div>
}
function Film({version}){
 const frame=useCurrentFrame(),brand=version==='first'?'FrameLab':'SignalCut',accent=version==='first'?'#25b9a5':'#f27d62';
 return <AbsoluteFill style={{background:'#0d161c',color:'#edf0eb',fontFamily:'R2Sans'}}>
  <style>{`@font-face{font-family:R2Serif;src:url(${staticFile('Georgia.ttf')})}@font-face{font-family:R2Sans;src:url(${staticFile('Arial.ttf')})}`}</style>
  <div style={{position:'absolute',left:52,top:34,font:'27px R2Serif',display:'flex',alignItems:'center',gap:12}}><b style={{background:accent,color:'#0d161c',padding:'5px 12px',borderRadius:8}}>{brand[0]}</b>{brand}<span style={{font:'19px R2Sans',letterSpacing:2,color:'#91a3a8',marginLeft:260}}>STORY → SCREEN → DELIVERY</span></div>
  <h1 style={{position:'absolute',left:440,top:180,font:'62px/1.1 Georgia',margin:0}}>Make the story<br/>easy to follow.</h1><p style={{position:'absolute',left:444,top:345,color:'#91a3a8',fontSize:23,lineHeight:1.6}}>A reproducible editing experiment.<br/>Fictitious product. Real pipeline.</p>
  <OffthreadVideo muted src={staticFile('clean.mp4')} style={{position:'absolute',left:52,top:160,width:340,height:380,objectFit:'cover',objectPosition:'left center',border:'1px solid #34434a',borderRadius:14}}/>
  {config.beats.map((s,i)=><Sequence key={s} from={s*30} durationInFrames={180}><Plate index={i} version={version} accent={accent}/></Sequence>)}
  {config.captions.map((c,i)=><Sequence key={i} from={Math.round(c.start*30)} durationInFrames={Math.max(1,Math.round(c.end*30)-Math.round(c.start*30))}><div style={{position:'absolute',bottom:38,left:128,width:1024,textAlign:'center',fontSize:30,fontWeight:500,background:'#080d11',padding:'13px 20px',borderRadius:8}}>{c.text}</div></Sequence>)}
 </AbsoluteFill>
}
registerRoot(()=> <Composition id="RoundTwo" component={Film} width={1280} height={720} fps={30} durationInFrames={config.frames} defaultProps={{version:'first'}}/>);

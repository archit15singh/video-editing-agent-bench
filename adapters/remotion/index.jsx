import React from 'react';
import {AbsoluteFill, Composition, OffthreadVideo, Sequence, registerRoot, staticFile, useCurrentFrame, interpolate} from 'remotion';
import manifest from '../../fixtures/manifest.json';
const kept=manifest.scenes.filter(s=>s.keep);
const Edit=({title})=>{
  const frame=useCurrentFrame();
  return <AbsoluteFill style={{backgroundColor:'#090f1b',fontFamily:'Arial'}}>
    {kept.map(s=><Sequence key={s.id} from={Math.round(s.edit_start*30)} durationInFrames={s.frames}>
      <OffthreadVideo src={staticFile("source.mp4")} trimBefore={Math.round(s.source_start*30)} />
      <div style={{position:'absolute',bottom:50,left:100,right:100,padding:'20px 26px',borderRadius:12,background:'#000c',color:'white',fontSize:30,textAlign:'center'}}>{s.text}</div>
    </Sequence>)}
    {frame<90&&<div style={{position:'absolute',top:170,left:80,color:'white',fontSize:58,fontWeight:700,opacity:interpolate(frame,[0,12,75,89],[0,1,1,0],{extrapolateRight:'clamp'}),transform:`translateY(${interpolate(frame,[0,15],[24,0],{extrapolateRight:'clamp'})}px)`}}>{title}</div>}
  </AbsoluteFill>;
};
registerRoot(()=> <Composition id="Benchmark" component={Edit} width={1280} height={720} fps={30} durationInFrames={kept.reduce((n,s)=>n+s.frames,0)} defaultProps={{title:manifest.title}}/>);

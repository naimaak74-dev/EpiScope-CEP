const csvPath = "../data/gold/daily_disease_summary.csv";
const dateCandidates=["date","report_date","encounter_date","visit_date","ds"];
const countCandidates=["case_count","cases","encounters","count","total_cases","n"];
const diseaseCandidates=["disease","disease_name","condition","diagnosis"];
const districtCandidates=["district","district_name","district_id","admin2"];
let allRows=[], selectedDisease="all", selectedDistrict="all";

function findCol(cols,candidates){const map=new Map(cols.map(c=>[c.toLowerCase(),c]));return candidates.map(c=>map.get(c)).find(Boolean);}
function normalize(rows){
 if(!rows.length) throw new Error("CSV has no data rows");
 const cols=Object.keys(rows[0]), dc=findCol(cols,dateCandidates), cc=findCol(cols,countCandidates);
 const dis=findCol(cols,diseaseCandidates), dist=findCol(cols,districtCandidates);
 if(!dc||!cc) throw new Error("Expected date and case-count columns. Found: "+cols.join(", "));
 return rows.map(r=>({date:new Date(r[dc]),cases:+r[cc],disease:dis?r[dis]:"All diseases",district:dist?r[dist]:"All districts"}))
 .filter(r=>!isNaN(r.date)&&Number.isFinite(r.cases));
}
function filtered(){return allRows.filter(r=>(selectedDisease==="all"||r.disease===selectedDisease)&&(selectedDistrict==="all"||r.district===selectedDistrict));}
function svgBase(id){const s=d3.select("#"+id);s.selectAll("*").remove();return s;}
function drawBars(id,data,labelKey,valueKey,click){
 const svg=svgBase(id), w=svg.node().clientWidth||600,h=260,m={top:10,right:15,bottom:50,left:48};
 svg.attr("viewBox",`0 0 ${w} ${h}`);
 const x=d3.scaleBand().domain(data.map(d=>d[labelKey])).range([m.left,w-m.right]).padding(.15);
 const y=d3.scaleLinear().domain([0,d3.max(data,d=>d[valueKey])||1]).nice().range([h-m.bottom,m.top]);
 svg.append("g").attr("transform",`translate(0,${h-m.bottom})`).call(d3.axisBottom(x).tickFormat(d=>String(d).slice(0,12))).selectAll("text").attr("transform","rotate(-25)").style("text-anchor","end");
 svg.append("g").attr("transform",`translate(${m.left},0)`).call(d3.axisLeft(y).ticks(5));
 svg.selectAll("rect").data(data).join("rect").attr("class","bar").attr("x",d=>x(d[labelKey])).attr("y",d=>y(d[valueKey])).attr("width",x.bandwidth()).attr("height",d=>y(0)-y(d[valueKey])).attr("fill","#287d8e").on("click",(e,d)=>click&&click(d));
}
function drawTrend(data){
 const daily=d3.rollups(data,v=>d3.sum(v,d=>d.cases),d=>d3.timeFormat("%Y-%m-%d")(d.date)).map(([date,cases])=>({date:new Date(date),cases})).sort((a,b)=>a.date-b.date);
 const svg=svgBase("trendView"),w=svg.node().clientWidth||600,h=260,m={top:10,right:15,bottom:35,left:48};svg.attr("viewBox",`0 0 ${w} ${h}`);
 const x=d3.scaleTime().domain(d3.extent(daily,d=>d.date)).range([m.left,w-m.right]),y=d3.scaleLinear().domain([0,d3.max(daily,d=>d.cases)||1]).nice().range([h-m.bottom,m.top]);
 svg.append("g").attr("transform",`translate(0,${h-m.bottom})`).call(d3.axisBottom(x).ticks(5));
 svg.append("g").attr("transform",`translate(${m.left},0)`).call(d3.axisLeft(y).ticks(5));
 svg.append("path").datum(daily).attr("fill","none").attr("stroke","#287d8e").attr("stroke-width",2).attr("d",d3.line().x(d=>x(d.date)).y(d=>y(d.cases)));
}
function drawHeat(data){
 const svg=svgBase("heatView"),w=svg.node().clientWidth||600,h=260,m={top:20,right:10,bottom:28,left:100};svg.attr("viewBox",`0 0 ${w} ${h}`);
 const rows=d3.rollups(data,v=>d3.mean(v,d=>d.cases),d=>d.disease,d=>d.date.getMonth()+1).flatMap(([disease,months])=>months.map(([month,value])=>({disease,month,value})));
 const diseases=[...new Set(rows.map(d=>d.disease))],months=d3.range(1,13);
 const x=d3.scaleBand().domain(months).range([m.left,w-m.right]).padding(.06),y=d3.scaleBand().domain(diseases).range([m.top,h-m.bottom]).padding(.06);
 const color=d3.scaleSequential(d3.interpolateYlOrRd).domain([0,d3.max(rows,d=>d.value)||1]);
 svg.append("g").attr("transform",`translate(0,${h-m.bottom})`).call(d3.axisBottom(x).tickFormat(d=>d3.timeFormat("%b")(new Date(2000,d-1,1))));
 svg.append("g").attr("transform",`translate(${m.left},0)`).call(d3.axisLeft(y));
 svg.selectAll("rect").data(rows).join("rect").attr("x",d=>x(d.month)).attr("y",d=>y(d.disease)).attr("width",x.bandwidth()).attr("height",y.bandwidth()).attr("fill",d=>color(d.value)).append("title").text(d=>`${d.disease}, month ${d.month}: mean ${d.value.toFixed(1)}`);
}
function drawResources(data){
 const totals=d3.rollups(data,v=>d3.sum(v,d=>d.cases),d=>d.district).map(([district,cases])=>({district,cases})).sort((a,b)=>b.cases-a.cases).slice(0,12);
 drawBars("resourceView",totals,"district","cases",d=>{selectedDistrict=d.district;document.querySelector("#district").value=d.district;render();});
}
function render(){
 const data=filtered();if(!data.length)return;
 const byDistrict=d3.rollups(data,v=>d3.sum(v,d=>d.cases),d=>d.district).map(([district,cases])=>({district,cases})).sort((a,b)=>b.cases-a.cases).slice(0,15);
 drawBars("districtView",byDistrict,"district","cases",d=>{selectedDistrict=d.district;document.querySelector("#district").value=d.district;render();});
 drawTrend(data);drawHeat(data);drawResources(data);
 const byDay=d3.rollups(data,v=>d3.sum(v,d=>d.cases),d=>d3.timeFormat("%Y-%m-%d")(d.date)).map(([date,cases])=>({date,cases})).sort((a,b)=>b.date.localeCompare(a.date)).slice(0,20);
 document.querySelector("#alerts").innerHTML="<table><thead><tr><th>Date</th><th>Disease</th><th>District</th><th>Count</th><th>Status</th></tr></thead><tbody>"+data.slice().sort((a,b)=>b.date-a.date).slice(0,30).map(r=>`<tr><td>${d3.timeFormat("%Y-%m-%d")(r.date)}</td><td>${r.disease}</td><td>${r.district}</td><td>${r.cases>0&&r.cases<5?"Suppressed":Math.round(r.cases)}</td><td>Review trend</td></tr>`).join("")+"</tbody></table>";
}
function initFilters(){
 const diseases=[...new Set(allRows.map(r=>r.disease))].sort(),districts=[...new Set(allRows.map(r=>r.district))].sort();
 d3.select("#disease").selectAll("option.item").data(diseases).join("option").attr("class","item").attr("value",d=>d).text(d=>d);
 d3.select("#district").selectAll("option.item").data(districts).join("option").attr("class","item").attr("value",d=>d).text(d=>d);
 document.querySelector("#disease").addEventListener("change",e=>{selectedDisease=e.target.value;render()});
 document.querySelector("#district").addEventListener("change",e=>{selectedDistrict=e.target.value;render()});
 document.querySelector("#reset").addEventListener("click",()=>{selectedDisease="all";selectedDistrict="all";document.querySelector("#disease").value="all";document.querySelector("#district").value="all";render()});
}
d3.csv(csvPath).then(rows=>{allRows=normalize(rows);initFilters();document.querySelector("#freshness").textContent="Latest date in file: "+d3.timeFormat("%Y-%m-%d")(d3.max(allRows,d=>d.date))+" · verify source freshness";render();})
.catch(err=>{document.querySelector("#freshness").textContent="Could not load Gold CSV.";document.querySelector("main").insertAdjacentHTML("afterbegin",`<div class="panel"><b>Dashboard data error:</b> ${err.message}. Check the CSV path and date/count column names.</div>`);});

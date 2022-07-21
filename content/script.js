const table = document.getElementById('main_table');
// resizableGrid(table);
table.addEventListener('click', onTrClick)

function getTextDiv(code){
  // return `<div style="display:grid; grid: 1fr 1fr/1fr 1fr">
  // <div><input type="checkbox"></div><div><pre style="margin:0">${code}</pre></div>
  // <div><input type="checkbox"></div><div><pre style="margin:0">     zcxvb</pre></div>
  // <div></div><div><pre></pre></div>
  // <div></div><div><pre></pre></div>
  // <div></div><div><pre></pre></div>
  // <div></div><div><pre></pre></div>
  // <div></div><div><pre></pre></div>
  // <div></div><div><pre></pre></div>
  // <div></div><div><pre></pre></div>
  // </div>`;
  let strs = json[code]["rows"]
  let tps = json[code]["types"]
  console.log(strs)
  console.log(tps)
  ret_str = '<div style="display:grid; grid: 1fr 1fr/1fr 1fr">'
  for (let i = 0; i<strs.length; i++)
    ret_str += `<div><input type="checkbox"></div><div class = "${tps[i]}"><pre style="margin:0">${strs[i]}</pre></div>`
  console.log(strs)
  console.log(tps)
  ret_str += '</div>'

  return ret_str;  
}

function onTrClick(e){
  let element = e.target;

  if (element.hasAttribute('code')){
    let row = element.parentElement
    let cells = row.cells

    console.log(cells)

    if (!row.hasAttribute("isExpand")){
      for (let i = 1; i<cells.length; i++){console.log(cells[i]); cells[i].innerHTML+= getTextDiv(cells[i].getAttribute("code"));}
      row.setAttribute("isExpand",'True')
    }
    else if (row.getAttribute("isExpand") == "True"){
      for (let i = 1; i<cells.length; i++){cells[i].children[0].setAttribute("hidden",'')}
      row.setAttribute("isExpand",'False')
    }
    else if (row.getAttribute("isExpand") == "False"){
      for (let i = 1; i<cells.length; i++){cells[i].children[0].removeAttribute("hidden")}
      row.setAttribute("isExpand",'True')
    }
  }
}
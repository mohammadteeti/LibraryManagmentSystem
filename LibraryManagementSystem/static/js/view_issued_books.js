
//ade out messages list 
$(document).ready(function() {
    
    
    $("#my-li").fadeOut(3000); // fade out over 3 seconds
    
    
    const copy_btn = document.getElementById('id_copy');
    const pdf_btn = document.getElementById('id_pdf');
    const csv_btn = document.getElementById('id_csv');
    const excel_btn = document.getElementById('id_excel');

   copy_btn.addEventListener('click',function(ev){
     ev.preventDefault();
     copyToClipoard();
   });

   pdf_btn.addEventListener('click',function(ev){
    ev.preventDefault();
    saveAsPDF();
  })

  csv_btn.addEventListener('click',function(ev){
    ev.preventDefault();
    const table=document.getElementById('issued_books_table');
    console.log(tableToCSV(table));

  })


  excel_btn.addEventListener('click',function(ev){
    ev.preventDefault();
    const table=document.getElementById('issued_books_table');
    exportToExcel(table)

  })



    
});

function copyToClipoard(){
    
 const range = document.createRange();
 const table=document.getElementById('issued_books_table');
 range.selectNode(table);
 window.getSelection().removeAllRanges();
 window.getSelection().addRange(range);
 document.execCommand('copy');

 const messagesDiv = document.querySelector('.messages-div');
 const messageList=document.getElementById('my-li');
 const li = document.getElementById('li1');
     if (li == null){
        messageList=document.createElement('ul');
        messageList.id='my-li';
        li=document.createElement('li');
        li.id='li1'


     }
 messageList.classList.add('messages');
 li.classList.add('alert');
 li.classList.add('alert-success');
 li.textContent='Table Copied To Clipboard!';


 $('my-li').fadeOut(3000); // fade out over 3 seconds
 messageList.style.display='block';
}




function saveAsPDF() {
const doc = new window.jspdf.jsPDF();
const table = document.getElementById('issued_books_table');
const toSaveTable=table.cloneNode(true);
const tableRows = toSaveTable.rows;

// remove last column from table rows
for (let i = 0; i < tableRows.length; i++) {
  tableRows[i].deleteCell(-1);
}

doc.autoTable({
  html: toSaveTable,
  startY: 20,
  styles: {
    cellPadding: 1,
    fontSize: 11,
    valign: 'middle',
    halign: 'center',
  },
});

doc.save('table.pdf');


}


function tableToCSV(table) {
    const rows = table.querySelectorAll('tr');
    const lines = [];
  
    for (let i = 0; i < rows.length; i++) {
      const cells = rows[i].querySelectorAll('td:not(:last-child), th:not(:last-child)');
      const line = Array.from(cells).map(cell => cell.innerText.replace(/(\r\n|\n|\r)/gm, '')).join(',');
      lines.push(line);
    }
  
    downloadCSV(lines.join('\n'),'table.csv');

  }

  function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: "text/csv" });
  
    const downloadLink = document.createElement("a");
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  }
  
  
  function exportToExcel(table) {
    // Get table data as array
    const toSaveTable=table.cloneNode(true);
    const tableRows = toSaveTable.rows;

// remove last column from table rows
for (let i = 0; i < tableRows.length; i++) {
  tableRows[i].deleteCell(-1);
}
    const rows = Array.from(tableRows).map(row => Array.from(row.cells).map(cell => cell.innerText));

    // Create workbook and worksheet
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(rows);

    // Add worksheet to workbook and save
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    XLSX.writeFile(wb, 'table.xlsx');
  }
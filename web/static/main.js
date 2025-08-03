document.addEventListener('DOMContentLoaded', func on() { 
    fetch('/api/data') 
        .then(response => response.json()) 
        .then(data => { 
            const tbody = document.querySelector('#dataTable tbody'); 
            data.forEach(item => { 
                const row = document.createElement('tr'); 
                row.innerHTML = ` 
                    <td class="py-2 px-4 border">${item['Channel Username'] || 'N/A'}</td> 
                    <td class="py-2 px-4 border">${item['Channel Title'] || 'N/A'}</td> 
                    <td class="py-2 px-4 border">${item['Descrip on'] || 'N/A'}</td> 
                    <td class="py-2 px-4 border">${item['Drug Content Detected'] || 'N/A'}</td> 
                    <td class="py-2 px-4 border">${item['Drug Probability'] || 'N/A'}</td> 
                    <td class="py-2 px-4 border">${item['Timestamp'] || 'N/A'}</td> 
                    <td class="py-2 px-4 border"> 
                        ${item['Image URL'] && item['Image URL'] !== 'No image available' ?  
                          `<img src="${item['Image URL']}" alt="Profile Picture" class="h-16 w-16 
object-cover rounded">` :  
                          'No image'} 
                    </td> 
                `; 
                tbody.appendChild(row); 
            }); 
        }) 
        .catch(error => { 
            console.error('Error fetching data:', error); 
            const tbody = document.querySelector('#dataTable tbody'); 
            tbody.innerHTML = '<tr><td colspan="7" class="py-2 px-4 border text-center text-red
500">Error loading data</td></tr>'; 
        }); 
}); 

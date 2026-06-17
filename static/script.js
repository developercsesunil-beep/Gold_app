// static/script.js

document.addEventListener("DOMContentLoaded", () => {
    initializeDates();
    loadGoldRate();
    // Load news for today initially
    loadNews();
});

function initializeDates() {
    const dropdown = document.getElementById("dateSelect");
    dropdown.innerHTML = ""; // Clear existing

    const today = new Date();

    for (let i = 0; i < 5; i++) {
        let date = new Date();
        date.setDate(today.getDate() - i);
        
        // Format as YYYY-MM-DD
        let formatted = date.toISOString().split("T")[0];
        
        let option = document.createElement("option");
        option.value = formatted;
        
        // Make the text more readable
        if (i === 0) {
            option.textContent = `Today (${formatted})`;
        } else if (i === 1) {
            option.textContent = `Yesterday (${formatted})`;
        } else {
            option.textContent = formatted;
        }

        dropdown.appendChild(option);
    }
}

async function loadGoldRate() {
    try {
        const response = await fetch("/gold-rate");
        if (!response.ok) throw new Error("Failed to fetch gold rate");
        
        const data = await response.json();
        
        // Animate counting up for effect
        animateValue("goldRate", 0, data.price, 1000);
        
        if (data.currency) {
            document.getElementById("goldCurrency").innerText = data.currency === "INR" ? "₹" : data.currency;
        }
        if (data.unit) {
            document.getElementById("goldUnit").innerText = `/${data.unit}`;
        }

    } catch (error) {
        console.error("Error fetching gold rate:", error);
        document.getElementById("goldRate").innerText = "Error";
    }
}

function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        // easeOutQuart
        const ease = 1 - Math.pow(1 - progress, 4);
        const current = (progress * (end - start) + start).toFixed(2);
        
        // Format with commas
        obj.innerHTML = parseFloat(current).toLocaleString('en-IN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
        
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

async function loadNews() {
    const date = document.getElementById("dateSelect").value;
    const container = document.getElementById("newsContainer");
    const loader = document.getElementById("loader");
    const dateDisplay = document.getElementById("newsDateDisplay");
    
    // Update display date
    const selectedText = document.getElementById("dateSelect").options[document.getElementById("dateSelect").selectedIndex].text;
    dateDisplay.innerText = selectedText.split(' ')[0] === 'Today' || selectedText.split(' ')[0] === 'Yesterday' 
        ? selectedText.split(' ')[0] 
        : date;

    // Show loader, hide grid
    container.innerHTML = "";
    loader.classList.remove("hidden");

    try {
        const response = await fetch(`/gold-news/${date}`);
        if (!response.ok) throw new Error("Failed to fetch news");
        
        const data = await response.json();
        
        loader.classList.add("hidden");

        if (!data.articles || data.articles.length === 0) {
            container.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-secondary);">
                    <h3>No news found for this date.</h3>
                    <p>Try selecting a different date.</p>
                </div>
            `;
            return;
        }

        let html = "";
        data.articles.forEach((article, index) => {
            // Only show articles with a title and url
            if (article.title && article.title !== "[Removed]") {
                // Stagger animation delay
                const delay = index * 0.1;
                
                const sourceName = article.source ? article.source.name : "News Source";
                const description = article.description || "Click to read the full article...";
                
                html += `
                <div class="card" style="animation: fadeUp 0.5s ease forwards ${delay}s; opacity: 0; transform: translateY(20px);">
                    <div class="card-source">${sourceName}</div>
                    <h3>${article.title}</h3>
                    <p>${description}</p>
                    <a href="${article.url}" class="read-more" target="_blank" rel="noopener noreferrer">
                        Read Full Article <span style="font-size: 1.2rem">→</span>
                    </a>
                </div>
                `;
            }
        });

        container.innerHTML = html;

    } catch (error) {
        console.error("Error fetching news:", error);
        loader.classList.add("hidden");
        container.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: #ef4444;">
                <h3>Error loading news</h3>
                <p>Please check your connection or try again later.</p>
            </div>
        `;
    }
}

// Add keyframes for the card entrance animation dynamically
const style = document.createElement('style');
style.innerHTML = `
    @keyframes fadeUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

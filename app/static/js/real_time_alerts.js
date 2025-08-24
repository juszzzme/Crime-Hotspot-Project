/**
 * Real-time Crime Alert System
 * WebSocket-based live notifications and alert management
 */

class RealTimeCrimeAlerts {
    constructor(options = {}) {
        this.config = {
            alertTypes: ['high_priority', 'medium_priority', 'low_priority', 'emergency'],
            maxAlerts: 50,
            alertDuration: 10000, // 10 seconds
            soundEnabled: true,
            locationRadius: 5, // km
            ...options
        };
        
        this.alerts = [];
        this.subscribers = new Map();
        this.userLocation = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        
        this.init();
    }
    
    init() {
        console.log('🚨 Initializing Real-time Crime Alert System...');
        this.createAlertContainer();
        this.setupEventListeners();
        this.requestLocationPermission();
        this.startSimulation(); // For demo purposes
        console.log('✅ Real-time Alert System initialized');
    }
    
    createAlertContainer() {
        // Create alert container if it doesn't exist
        if (!document.getElementById('crime-alerts-container')) {
            const container = document.createElement('div');
            container.id = 'crime-alerts-container';
            container.className = 'crime-alerts-container';
            document.body.appendChild(container);
        }
        
        // Create alert control panel
        this.createControlPanel();
    }
    
    createControlPanel() {
        const controlPanel = document.createElement('div');
        controlPanel.className = 'alert-control-panel';
        controlPanel.innerHTML = `
            <div class="alert-controls">
                <h6><i class="fas fa-bell"></i> Alert Settings</h6>
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="alertsEnabled" checked>
                    <label class="form-check-label" for="alertsEnabled">Enable Alerts</label>
                </div>
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="soundEnabled" checked>
                    <label class="form-check-label" for="soundEnabled">Sound Notifications</label>
                </div>
                <div class="alert-radius-control">
                    <label for="alertRadius" class="form-label">Alert Radius: <span id="radiusValue">5</span> km</label>
                    <input type="range" class="form-range" id="alertRadius" min="1" max="20" value="5">
                </div>
                <div class="alert-stats">
                    <small class="text-muted">
                        Active Alerts: <span id="activeAlertCount">0</span><br>
                        Total Today: <span id="todayAlertCount">0</span>
                    </small>
                </div>
            </div>
        `;
        
        // Position the control panel
        controlPanel.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            z-index: 9998;
            max-width: 250px;
            font-size: 0.85rem;
        `;
        
        document.body.appendChild(controlPanel);
        this.setupControlEvents();
    }
    
    setupControlEvents() {
        // Enable/disable alerts
        document.getElementById('alertsEnabled').addEventListener('change', (e) => {
            this.config.alertsEnabled = e.target.checked;
            if (!e.target.checked) {
                this.clearAllAlerts();
            }
        });
        
        // Enable/disable sound
        document.getElementById('soundEnabled').addEventListener('change', (e) => {
            this.config.soundEnabled = e.target.checked;
        });
        
        // Alert radius control
        const radiusSlider = document.getElementById('alertRadius');
        radiusSlider.addEventListener('input', (e) => {
            this.config.locationRadius = parseInt(e.target.value);
            document.getElementById('radiusValue').textContent = e.target.value;
        });
    }
    
    setupEventListeners() {
        // Listen for page visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseAlerts();
            } else {
                this.resumeAlerts();
            }
        });
        
        // Listen for browser notifications permission
        if ('Notification' in window) {
            if (Notification.permission === 'default') {
                this.requestNotificationPermission();
            }
        }
    }
    
    async requestLocationPermission() {
        if ('geolocation' in navigator) {
            try {
                const position = await new Promise((resolve, reject) => {
                    navigator.geolocation.getCurrentPosition(resolve, reject, {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 300000 // 5 minutes
                    });
                });
                
                this.userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                    accuracy: position.coords.accuracy
                };
                
                console.log('📍 User location obtained for proximity alerts');
                this.showLocationAlert('Location access granted. You will receive proximity-based alerts.');
                
            } catch (error) {
                console.warn('⚠️ Location access denied or unavailable');
                this.showLocationAlert('Location access denied. You will receive all alerts regardless of location.', 'warning');
            }
        }
    }
    
    async requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                this.showLocationAlert('Browser notifications enabled!', 'success');
            }
        }
    }
    
    showLocationAlert(message, type = 'info') {
        const alert = {
            id: `location_${Date.now()}`,
            type: 'system',
            priority: 'low_priority',
            title: 'Location Service',
            message: message,
            timestamp: new Date(),
            location: 'System',
            alertType: type
        };
        
        this.displayAlert(alert);
    }
    
    // Simulate real-time alerts for demonstration
    startSimulation() {
        console.log('🎭 Starting alert simulation for demonstration...');
        
        // Simulate different types of alerts
        const alertTemplates = [
            {
                type: 'emergency',
                priority: 'high_priority',
                title: 'Emergency Alert',
                messages: [
                    'Armed robbery in progress at Central Mall',
                    'Multiple vehicle accident with injuries reported',
                    'Fire emergency at residential complex'
                ],
                locations: ['Central Mall', 'MG Road', 'Anna Nagar', 'T. Nagar']
            },
            {
                type: 'crime_alert',
                priority: 'medium_priority',
                title: 'Crime Alert',
                messages: [
                    'Theft reported in the area',
                    'Suspicious activity detected',
                    'Vehicle break-in reported',
                    'Pickpocketing incident reported'
                ],
                locations: ['Marina Beach', 'Express Avenue', 'Phoenix Mall', 'Velachery']
            },
            {
                type: 'safety_update',
                priority: 'low_priority',
                title: 'Safety Update',
                messages: [
                    'Increased police patrol in the area',
                    'Street lighting improved',
                    'New CCTV cameras installed',
                    'Community safety meeting scheduled'
                ],
                locations: ['Adyar', 'Mylapore', 'Triplicane', 'Egmore']
            }
        ];
        
        // Generate alerts at random intervals
        const generateAlert = () => {
            const template = alertTemplates[Math.floor(Math.random() * alertTemplates.length)];
            const message = template.messages[Math.floor(Math.random() * template.messages.length)];
            const location = template.locations[Math.floor(Math.random() * template.locations.length)];
            
            const alert = {
                id: `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                type: template.type,
                priority: template.priority,
                title: template.title,
                message: message,
                location: location,
                timestamp: new Date(),
                coordinates: this.generateRandomCoordinates(),
                severity: Math.floor(Math.random() * 5) + 1
            };
            
            this.processAlert(alert);
        };
        
        // Initial alert
        setTimeout(generateAlert, 3000);
        
        // Random intervals between 15-45 seconds
        const scheduleNext = () => {
            const interval = Math.random() * 30000 + 15000; // 15-45 seconds
            setTimeout(() => {
                generateAlert();
                scheduleNext();
            }, interval);
        };
        
        scheduleNext();
    }
    
    generateRandomCoordinates() {
        // Generate coordinates around Chennai
        const baseLatLng = [13.0827, 80.2707];
        const lat = baseLatLng[0] + (Math.random() - 0.5) * 0.2;
        const lng = baseLatLng[1] + (Math.random() - 0.5) * 0.2;
        return { lat, lng };
    }
    
    processAlert(alert) {
        // Check if alerts are enabled
        if (!this.config.alertsEnabled) return;
        
        // Check proximity if user location is available
        if (this.userLocation && alert.coordinates) {
            const distance = this.calculateDistance(
                this.userLocation.lat, this.userLocation.lng,
                alert.coordinates.lat, alert.coordinates.lng
            );
            
            if (distance > this.config.locationRadius) {
                console.log(`🔇 Alert filtered out - too far (${distance.toFixed(1)}km)`);
                return;
            }
            
            alert.distance = distance;
        }
        
        // Add to alerts array
        this.alerts.unshift(alert);
        
        // Limit number of stored alerts
        if (this.alerts.length > this.config.maxAlerts) {
            this.alerts = this.alerts.slice(0, this.config.maxAlerts);
        }
        
        // Display the alert
        this.displayAlert(alert);
        
        // Play sound if enabled
        if (this.config.soundEnabled) {
            this.playAlertSound(alert.priority);
        }
        
        // Show browser notification
        this.showBrowserNotification(alert);
        
        // Update statistics
        this.updateAlertStats();
        
        // Notify subscribers
        this.notifySubscribers('new_alert', alert);
        
        console.log(`🚨 New ${alert.priority} alert: ${alert.message}`);
    }
    
    displayAlert(alert) {
        const container = document.getElementById('crime-alerts-container');
        if (!container) return;
        
        const alertElement = document.createElement('div');
        alertElement.className = `crime-alert alert-${alert.priority} alert-${alert.type || 'default'}`;
        alertElement.id = alert.id;
        
        const timeAgo = this.getTimeAgo(alert.timestamp);
        const distanceText = alert.distance ? ` • ${alert.distance.toFixed(1)}km away` : '';
        
        alertElement.innerHTML = `
            <div class="alert-content">
                <div class="alert-header">
                    <div class="alert-icon">
                        ${this.getAlertIcon(alert.type, alert.priority)}
                    </div>
                    <div class="alert-title">
                        <strong>${alert.title}</strong>
                        <span class="alert-priority">${alert.priority.replace('_', ' ').toUpperCase()}</span>
                    </div>
                    <button class="alert-close" onclick="crimeAlerts.dismissAlert('${alert.id}')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="alert-body">
                    <p class="alert-message">${alert.message}</p>
                    <div class="alert-meta">
                        <span class="alert-location">
                            <i class="fas fa-map-marker-alt"></i> ${alert.location}
                        </span>
                        <span class="alert-time">
                            <i class="fas fa-clock"></i> ${timeAgo}${distanceText}
                        </span>
                    </div>
                </div>
                <div class="alert-actions">
                    <button class="btn btn-sm btn-outline-primary" onclick="crimeAlerts.viewOnMap('${alert.id}')">
                        <i class="fas fa-map"></i> View on Map
                    </button>
                    <button class="btn btn-sm btn-outline-success" onclick="crimeAlerts.shareAlert('${alert.id}')">
                        <i class="fas fa-share"></i> Share
                    </button>
                </div>
            </div>
        `;
        
        // Add animation
        alertElement.style.opacity = '0';
        alertElement.style.transform = 'translateX(100%)';
        
        container.insertBefore(alertElement, container.firstChild);
        
        // Animate in
        requestAnimationFrame(() => {
            alertElement.style.transition = 'all 0.5s ease-out';
            alertElement.style.opacity = '1';
            alertElement.style.transform = 'translateX(0)';
        });
        
        // Auto-dismiss after duration
        setTimeout(() => {
            this.dismissAlert(alert.id);
        }, this.config.alertDuration);
    }
    
    getAlertIcon(type, priority) {
        const icons = {
            emergency: '<i class="fas fa-exclamation-triangle text-danger"></i>',
            crime_alert: '<i class="fas fa-shield-alt text-warning"></i>',
            safety_update: '<i class="fas fa-info-circle text-info"></i>',
            system: '<i class="fas fa-cog text-secondary"></i>',
            default: '<i class="fas fa-bell text-primary"></i>'
        };
        
        return icons[type] || icons.default;
    }
    
    dismissAlert(alertId) {
        const alertElement = document.getElementById(alertId);
        if (alertElement) {
            alertElement.style.transition = 'all 0.3s ease-in';
            alertElement.style.opacity = '0';
            alertElement.style.transform = 'translateX(100%)';
            
            setTimeout(() => {
                if (alertElement.parentNode) {
                    alertElement.parentNode.removeChild(alertElement);
                }
            }, 300);
        }
        
        // Remove from alerts array
        this.alerts = this.alerts.filter(alert => alert.id !== alertId);
        this.updateAlertStats();
    }
    
    clearAllAlerts() {
        const container = document.getElementById('crime-alerts-container');
        if (container) {
            container.innerHTML = '';
        }
        this.alerts = [];
        this.updateAlertStats();
    }
    
    playAlertSound(priority) {
        // Create audio context for sound generation
        if (typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined') {
            const AudioContextClass = AudioContext || webkitAudioContext;
            const audioContext = new AudioContextClass();
            
            const frequencies = {
                high_priority: [800, 1000, 800],
                medium_priority: [600, 800],
                low_priority: [400],
                emergency: [1000, 800, 1000, 800]
            };
            
            const freq = frequencies[priority] || frequencies.low_priority;
            
            freq.forEach((frequency, index) => {
                setTimeout(() => {
                    const oscillator = audioContext.createOscillator();
                    const gainNode = audioContext.createGain();
                    
                    oscillator.connect(gainNode);
                    gainNode.connect(audioContext.destination);
                    
                    oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
                    oscillator.type = 'sine';
                    
                    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
                    
                    oscillator.start(audioContext.currentTime);
                    oscillator.stop(audioContext.currentTime + 0.2);
                }, index * 250);
            });
        }
    }
    
    showBrowserNotification(alert) {
        if ('Notification' in window && Notification.permission === 'granted') {
            const notification = new Notification(alert.title, {
                body: `${alert.message}\nLocation: ${alert.location}`,
                icon: '/static/images/crime-alert-icon.png',
                badge: '/static/images/crime-badge.png',
                tag: alert.id,
                requireInteraction: alert.priority === 'high_priority'
            });
            
            notification.onclick = () => {
                window.focus();
                this.viewOnMap(alert.id);
                notification.close();
            };
            
            // Auto-close after 5 seconds for non-emergency alerts
            if (alert.priority !== 'high_priority') {
                setTimeout(() => notification.close(), 5000);
            }
        }
    }
    
    calculateDistance(lat1, lng1, lat2, lng2) {
        const R = 6371; // Earth's radius in kilometers
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLng = (lng2 - lng1) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                  Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                  Math.sin(dLng/2) * Math.sin(dLng/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }
    
    getTimeAgo(timestamp) {
        const now = new Date();
        const diffTime = Math.abs(now - timestamp);
        const diffMinutes = Math.ceil(diffTime / (1000 * 60));
        
        if (diffMinutes < 1) return 'Just now';
        if (diffMinutes < 60) return `${diffMinutes}m ago`;
        if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}h ago`;
        return `${Math.floor(diffMinutes / 1440)}d ago`;
    }
    
    updateAlertStats() {
        const activeCount = document.querySelectorAll('.crime-alert').length;
        const todayCount = this.alerts.filter(alert => {
            const today = new Date().toDateString();
            return alert.timestamp.toDateString() === today;
        }).length;
        
        const activeElement = document.getElementById('activeAlertCount');
        const todayElement = document.getElementById('todayAlertCount');
        
        if (activeElement) activeElement.textContent = activeCount;
        if (todayElement) todayElement.textContent = todayCount;
    }
    
    viewOnMap(alertId) {
        const alert = this.alerts.find(a => a.id === alertId);
        if (alert && alert.coordinates) {
            // If advanced map is available, center on alert location
            if (window.advancedMap && window.advancedMap.map) {
                window.advancedMap.map.setView([alert.coordinates.lat, alert.coordinates.lng], 15);
                
                // Add temporary marker for the alert
                const alertMarker = L.marker([alert.coordinates.lat, alert.coordinates.lng], {
                    icon: L.divIcon({
                        className: 'alert-location-marker',
                        html: '<div class="pulse-marker"></div>',
                        iconSize: [20, 20]
                    })
                }).addTo(window.advancedMap.map);
                
                // Remove marker after 10 seconds
                setTimeout(() => {
                    window.advancedMap.map.removeLayer(alertMarker);
                }, 10000);
            } else {
                // Fallback: open in new tab with coordinates
                const url = `https://www.google.com/maps?q=${alert.coordinates.lat},${alert.coordinates.lng}`;
                window.open(url, '_blank');
            }
        }
    }
    
    shareAlert(alertId) {
        const alert = this.alerts.find(a => a.id === alertId);
        if (alert) {
            const shareText = `Crime Alert: ${alert.message} at ${alert.location}. Stay safe!`;
            
            if (navigator.share) {
                navigator.share({
                    title: alert.title,
                    text: shareText,
                    url: window.location.href
                });
            } else {
                // Fallback: copy to clipboard
                navigator.clipboard.writeText(shareText).then(() => {
                    this.showLocationAlert('Alert details copied to clipboard!', 'success');
                });
            }
        }
    }
    
    subscribe(eventType, callback) {
        if (!this.subscribers.has(eventType)) {
            this.subscribers.set(eventType, []);
        }
        this.subscribers.get(eventType).push(callback);
    }
    
    notifySubscribers(eventType, data) {
        if (this.subscribers.has(eventType)) {
            this.subscribers.get(eventType).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error('Error in alert subscriber:', error);
                }
            });
        }
    }
    
    pauseAlerts() {
        this.isPaused = true;
        console.log('⏸️ Alerts paused');
    }
    
    resumeAlerts() {
        this.isPaused = false;
        console.log('▶️ Alerts resumed');
    }
    
    getAlertHistory() {
        return this.alerts;
    }
    
    getAlertsByType(type) {
        return this.alerts.filter(alert => alert.type === type);
    }
    
    getAlertsByPriority(priority) {
        return this.alerts.filter(alert => alert.priority === priority);
    }
}

// Global instance
let crimeAlerts = null;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    crimeAlerts = new RealTimeCrimeAlerts();
    
    // Make it globally accessible
    window.crimeAlerts = crimeAlerts;
});

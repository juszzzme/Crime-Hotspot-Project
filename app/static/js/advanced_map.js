/**
 * Advanced Crime Hotspot Map with AI-Powered Features
 * Enhanced visualizations, real-time updates, and interactive elements
 */

class AdvancedCrimeMap {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.map = null;
        this.markers = new Map();
        this.heatmapLayer = null;
        this.clusterGroup = null;
        this.crimeData = [];
        this.currentTimeFilter = 'all';
        this.currentCrimeFilter = 'all';
        
        // Configuration
        this.config = {
            defaultCenter: [13.0827, 80.2707], // Chennai coordinates
            defaultZoom: 11,
            heatmapRadius: 25,
            clusterRadius: 50,
            updateInterval: 30000, // 30 seconds for real-time updates
            ...options
        };
        
        this.init();
    }
    
    init() {
        console.log('Initializing Advanced Crime Map...');
        this.createMap();
        this.setupLayers();
        this.loadCrimeData();
        this.setupControls();
        this.startRealTimeUpdates();
        console.log('Advanced Crime Map initialized successfully');
    }
    
    createMap() {
        // Initialize Leaflet map with enhanced styling
        this.map = L.map(this.containerId, {
            center: this.config.defaultCenter,
            zoom: this.config.defaultZoom,
            zoomControl: false,
            attributionControl: false
        });
        
        // Add custom zoom control
        L.control.zoom({
            position: 'topright'
        }).addTo(this.map);
        
        // Add multiple tile layers for different views
        this.tileLayers = {
            street: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }),
            light: L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                attribution: '© CartoDB',
                subdomains: 'abcd',
                maxZoom: 20
            }),
            dark: L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '© CartoDB',
                subdomains: 'abcd',
                maxZoom: 20
            }),
            satellite: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                attribution: '© Esri',
                maxZoom: 19
            })
        };

        // Set default layer to match the interactive map (OpenStreetMap)
        this.tileLayers.street.addTo(this.map);

        // Set the default layer name for the layer control
        this.defaultLayer = 'street';

        // Add layer control
        L.control.layers(this.tileLayers, {}, {
            position: 'topright'
        }).addTo(this.map);
    }
    
    setupLayers() {
        // Initialize marker cluster group
        this.clusterGroup = L.markerClusterGroup({
            chunkedLoading: true,
            spiderfyOnMaxZoom: true,
            showCoverageOnHover: false,
            zoomToBoundsOnClick: true,
            maxClusterRadius: this.config.clusterRadius,
            iconCreateFunction: (cluster) => this.createClusterIcon(cluster)
        });
        
        // Initialize heatmap layer
        this.heatmapLayer = L.heatLayer([], {
            radius: this.config.heatmapRadius,
            blur: 15,
            maxZoom: 17,
            gradient: {
                0.0: '#313695',
                0.1: '#4575b4',
                0.2: '#74add1',
                0.4: '#abd9e9',
                0.6: '#fee090',
                0.8: '#fdae61',
                1.0: '#d73027'
            }
        });
        
        this.map.addLayer(this.clusterGroup);
    }
    
    createClusterIcon(cluster) {
        const childCount = cluster.getChildCount();
        const markers = cluster.getAllChildMarkers();
        
        // Analyze crime types in cluster
        const crimeTypes = {};
        markers.forEach(marker => {
            const crimeType = marker.options.crimeType || 'unknown';
            crimeTypes[crimeType] = (crimeTypes[crimeType] || 0) + 1;
        });
        
        // Determine dominant crime type
        const dominantType = Object.keys(crimeTypes).reduce((a, b) => 
            crimeTypes[a] > crimeTypes[b] ? a : b
        );
        
        // Get color based on dominant crime type
        const color = this.getCrimeTypeColor(dominantType);
        
        let className = 'marker-cluster ';
        if (childCount < 10) {
            className += 'marker-cluster-small';
        } else if (childCount < 100) {
            className += 'marker-cluster-medium';
        } else {
            className += 'marker-cluster-large';
        }
        
        return new L.DivIcon({
            html: `<div style="background-color: ${color}"><span>${childCount}</span></div>`,
            className: className,
            iconSize: new L.Point(40, 40)
        });
    }
    
    getCrimeTypeColor(crimeType) {
        const colors = {
            'murder': '#d73027',
            'rape': '#f46d43',
            'robbery': '#fdae61',
            'assault': '#fee08b',
            'burglary': '#e6f598',
            'theft': '#abdda4',
            'vandalism': '#66c2a5',
            'drug': '#3288bd',
            'unknown': '#5e4fa2'
        };
        return colors[crimeType.toLowerCase()] || colors.unknown;
    }
    
    createCrimeMarker(incident) {
        const color = this.getCrimeTypeColor(incident.crime_type);
        const severity = this.getCrimeSeverity(incident.crime_type);

        // Use original authentic circle markers from backup (like interactive map)
        const marker = L.circleMarker([incident.latitude, incident.longitude], {
            radius: 8,
            fillColor: color,
            color: '#fff',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8,
            crimeType: incident.crime_type,
            severity: severity,
            incident: incident
        });

        // Create detailed popup
        const popupContent = this.createPopupContent(incident);
        marker.bindPopup(popupContent, {
            maxWidth: 300,
            className: 'crime-popup'
        });

        return marker;
    }


    
    getCrimeIcon(crimeType) {
        const icons = {
            'murder': 'fa-skull',
            'rape': 'fa-exclamation-triangle',
            'robbery': 'fa-mask',
            'assault': 'fa-fist-raised',
            'burglary': 'fa-home',
            'theft': 'fa-hand-holding',
            'vandalism': 'fa-hammer',
            'drug': 'fa-pills',
            'unknown': 'fa-question'
        };
        return icons[crimeType.toLowerCase()] || icons.unknown;
    }
    
    getCrimeSeverity(crimeType) {
        const severityMap = {
            'murder': 5,
            'rape': 5,
            'assault': 4,
            'robbery': 4,
            'burglary': 3,
            'theft': 2,
            'vandalism': 2,
            'drug': 3,
            'unknown': 1
        };
        return severityMap[crimeType.toLowerCase()] || 1;
    }
    
    darkenColor(color) {
        // Simple color darkening function
        const hex = color.replace('#', '');
        const r = Math.max(0, parseInt(hex.substr(0, 2), 16) - 30);
        const g = Math.max(0, parseInt(hex.substr(2, 2), 16) - 30);
        const b = Math.max(0, parseInt(hex.substr(4, 2), 16) - 30);
        return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    }
    
    createPopupContent(incident) {
        const timeAgo = this.getTimeAgo(incident.date);
        const severity = this.getCrimeSeverity(incident.crime_type);
        const severityStars = '★'.repeat(severity) + '☆'.repeat(5 - severity);
        
        return `
            <div class="crime-popup-content">
                <div class="crime-header">
                    <h4><i class="fas ${this.getCrimeIcon(incident.crime_type)}"></i> ${incident.crime_type}</h4>
                    <span class="crime-severity" title="Severity Level">${severityStars}</span>
                </div>
                <div class="crime-details">
                    <p><strong>Location:</strong> ${incident.location || 'Unknown'}</p>
                    <p><strong>Date:</strong> ${incident.date} (${timeAgo})</p>
                    <p><strong>Time:</strong> ${incident.time || 'Unknown'}</p>
                    <p><strong>Description:</strong> ${incident.description || 'No details available'}</p>
                </div>
                <div class="crime-actions">
                    <button class="btn btn-sm btn-primary" onclick="advancedMap.showIncidentDetails('${incident.id}')">
                        <i class="fas fa-info-circle"></i> More Details
                    </button>
                    <button class="btn btn-sm btn-warning" onclick="advancedMap.reportSimilar('${incident.id}')">
                        <i class="fas fa-flag"></i> Report Similar
                    </button>
                </div>
            </div>
        `;
    }
    
    getTimeAgo(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) return '1 day ago';
        if (diffDays < 7) return `${diffDays} days ago`;
        if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`;
        return `${Math.ceil(diffDays / 30)} months ago`;
    }
    
    async loadCrimeData() {
        try {
            console.log('📊 Loading crime data...');

            // For demonstration, generate realistic crime data
            this.crimeData = this.generateSampleCrimeData();

            // Load infrastructure markers like the original interactive map
            this.loadInfrastructureMarkers();

            // In a real application, you would fetch from API:
            // const response = await fetch('/api/crime-incidents');
            // this.crimeData = await response.json();

            this.updateMapData();
            console.log(`✅ Loaded ${this.crimeData.length} crime incidents`);
        } catch (error) {
            console.error('❌ Error loading crime data:', error);
            this.showError('Failed to load crime data');
        }
    }

    loadInfrastructureMarkers() {
        // Add infrastructure markers exactly like the original interactive map
        const infrastructure = {
            'chennai': {
                hospitals: [
                    { lat: 13.0569, lng: 80.2425, name: 'Apollo Hospital Chennai' },
                    { lat: 13.0878, lng: 80.2785, name: 'Fortis Malar Hospital' },
                    { lat: 13.0827, lng: 80.2707, name: 'MIOT International' },
                    { lat: 13.0067, lng: 80.2206, name: 'Sri Ramachandra Medical Centre' },
                    { lat: 13.1185, lng: 80.2574, name: 'Government General Hospital' },
                    { lat: 13.0732, lng: 80.2609, name: 'Vijaya Hospital' }
                ],
                policeStations: [
                    { lat: 13.0827, lng: 80.2707, name: 'T. Nagar Police Station' },
                    { lat: 13.0878, lng: 80.2785, name: 'Anna Nagar Police Station' },
                    { lat: 13.0569, lng: 80.2425, name: 'Adyar Police Station' },
                    { lat: 13.1185, lng: 80.2574, name: 'Egmore Police Station' },
                    { lat: 13.0732, lng: 80.2609, name: 'Mylapore Police Station' }
                ],
                fireStations: [
                    { lat: 13.0827, lng: 80.2707, name: 'Chennai Fire Station - Central' },
                    { lat: 13.0878, lng: 80.2785, name: 'Anna Nagar Fire Station' },
                    { lat: 13.0569, lng: 80.2425, name: 'Adyar Fire Station' }
                ]
            }
        };

        const data = infrastructure['chennai'];
        if (data) {
            // Add hospital markers with red cross style
            data.hospitals?.forEach(hospital => {
                this.addInfrastructureMarker(hospital, 'hospital');
            });

            // Add police station markers with blue style
            data.policeStations?.forEach(station => {
                this.addInfrastructureMarker(station, 'police');
            });

            // Add fire station markers with orange style
            data.fireStations?.forEach(station => {
                this.addInfrastructureMarker(station, 'fire');
            });
        }
    }

    addInfrastructureMarker(facility, type) {
        // Use original authentic circle markers for infrastructure exactly like interactive map
        const colors = {
            hospital: '#e74c3c',  // Red (like original crime markers)
            police: '#3498db',    // Blue (like original crime markers)
            fire: '#f39c12',      // Orange (like original crime markers)
            school: '#2c3e50'     // Dark blue (like original crime markers)
        };

        const marker = L.circleMarker([facility.lat, facility.lng], {
            radius: 8,
            fillColor: colors[type] || '#2c3e50',
            color: '#fff',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        });

        marker.bindPopup(`
            <div class="crime-popup">
                <h6>${facility.name.toUpperCase()}</h6>
                <p><strong>Type:</strong> ${type.charAt(0).toUpperCase() + type.slice(1)}</p>
                <p><strong>Description:</strong> ${type} facility</p>
            </div>
        `);

        // Add marker to cluster group instead of directly to map
        this.clusterGroup.addLayer(marker);
        this.markers.set(facility.name, marker);
    }
    
    generateSampleCrimeData() {
        const crimeTypes = ['murder', 'rape', 'robbery', 'assault', 'burglary', 'theft', 'vandalism', 'drug'];
        const locations = [
            'T. Nagar', 'Anna Nagar', 'Adyar', 'Velachery', 'Tambaram',
            'Chrompet', 'Porur', 'OMR', 'ECR', 'Mylapore', 'Triplicane'
        ];

        const incidents = [];
        const baseLatLng = [13.0827, 80.2707]; // Chennai center

        for (let i = 0; i < 150; i++) {
            // Generate random coordinates around Chennai with land validation
            let lat, lng;
            let attempts = 0;
            do {
                lat = baseLatLng[0] + (Math.random() - 0.5) * 0.3;
                lng = baseLatLng[1] + (Math.random() - 0.5) * 0.3;
                attempts++;
            } while (!this.isOnLand(lat, lng) && attempts < 10);

            // If we couldn't find a land coordinate after 10 attempts, use a known land location
            if (attempts >= 10) {
                const landLocations = [
                    [13.0827, 80.2707], // T. Nagar
                    [13.0569, 80.2425], // Adyar
                    [13.1185, 80.2574], // Anna Nagar
                    [13.0067, 80.2206], // Velachery
                    [13.0878, 80.2785]  // Mylapore
                ];
                const randomLandLocation = landLocations[Math.floor(Math.random() * landLocations.length)];
                lat = randomLandLocation[0] + (Math.random() - 0.5) * 0.01; // Small variation
                lng = randomLandLocation[1] + (Math.random() - 0.5) * 0.01;
            }
            
            // Generate random date within last 30 days
            const date = new Date();
            date.setDate(date.getDate() - Math.floor(Math.random() * 30));
            
            incidents.push({
                id: `incident_${i}`,
                crime_type: crimeTypes[Math.floor(Math.random() * crimeTypes.length)],
                latitude: lat,
                longitude: lng,
                location: locations[Math.floor(Math.random() * locations.length)],
                date: date.toISOString().split('T')[0],
                time: `${Math.floor(Math.random() * 24).toString().padStart(2, '0')}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`,
                description: 'Sample incident for demonstration purposes',
                severity: Math.floor(Math.random() * 5) + 1
            });
        }
        
        return incidents;
    }
    
    updateMapData() {
        // Clear existing markers
        this.clusterGroup.clearLayers();
        this.markers.clear();
        
        // Filter data based on current filters
        const filteredData = this.filterCrimeData();
        
        // Add markers to cluster group
        filteredData.forEach(incident => {
            const marker = this.createCrimeMarker(incident);
            this.clusterGroup.addLayer(marker);
            this.markers.set(incident.id, marker);
        });
        
        // Update heatmap
        this.updateHeatmap(filteredData);
    }
    
    filterCrimeData() {
        return this.crimeData.filter(incident => {
            // Time filter
            if (this.currentTimeFilter !== 'all') {
                const incidentDate = new Date(incident.date);
                const now = new Date();
                const daysDiff = (now - incidentDate) / (1000 * 60 * 60 * 24);
                
                switch (this.currentTimeFilter) {
                    case 'today':
                        if (daysDiff > 1) return false;
                        break;
                    case 'week':
                        if (daysDiff > 7) return false;
                        break;
                    case 'month':
                        if (daysDiff > 30) return false;
                        break;
                }
            }
            
            // Crime type filter
            if (this.currentCrimeFilter !== 'all' && incident.crime_type !== this.currentCrimeFilter) {
                return false;
            }
            
            return true;
        });
    }
    
    updateHeatmap(data) {
        const heatmapData = data.map(incident => [
            incident.latitude,
            incident.longitude,
            incident.severity / 5 // Normalize severity to 0-1
        ]);
        
        this.heatmapLayer.setLatLngs(heatmapData);
    }



    isOnLand(lat, lng) {
        // Chennai land boundary validation
        // This is a simplified polygon check for Chennai's approximate land boundaries
        // Excludes major water bodies like Bay of Bengal and Adyar River areas

        // Basic Chennai city bounds (excluding ocean areas)
        const chennaiLandBounds = {
            north: 13.2,
            south: 12.9,
            east: 80.35,   // Reduced to exclude ocean
            west: 80.1
        };

        // Check if coordinates are within basic bounds
        if (lat < chennaiLandBounds.south || lat > chennaiLandBounds.north ||
            lng < chennaiLandBounds.west || lng > chennaiLandBounds.east) {
            return false;
        }

        // Exclude specific ocean/water areas
        const waterAreas = [
            // Bay of Bengal (eastern coast)
            { minLat: 12.9, maxLat: 13.2, minLng: 80.25, maxLng: 80.35 },
            // Adyar River mouth area
            { minLat: 13.0, maxLat: 13.05, minLng: 80.24, maxLng: 80.28 },
            // Cooum River mouth area
            { minLat: 13.08, maxLat: 13.09, minLng: 80.28, maxLng: 80.32 }
        ];

        // Check if point is in any water area
        for (const area of waterAreas) {
            if (lat >= area.minLat && lat <= area.maxLat &&
                lng >= area.minLng && lng <= area.maxLng) {
                return false;
            }
        }

        return true;
    }
    
    setupControls() {
        // Add custom control panel
        const controlPanel = L.control({ position: 'topleft' });
        
        controlPanel.onAdd = () => {
            const div = L.DomUtil.create('div', 'map-controls');
            div.innerHTML = `
                <div class="control-panel">
                    <h5><i class="fas fa-filter"></i> Filters</h5>
                    
                    <div class="filter-group">
                        <label>Time Period:</label>
                        <select id="timeFilter" class="form-select form-select-sm">
                            <option value="all">All Time</option>
                            <option value="today">Today</option>
                            <option value="week">This Week</option>
                            <option value="month">This Month</option>
                        </select>
                    </div>
                    
                    <div class="filter-group">
                        <label>Crime Type:</label>
                        <select id="crimeFilter" class="form-select form-select-sm">
                            <option value="all">All Types</option>
                            <option value="murder">Murder</option>
                            <option value="rape">Rape</option>
                            <option value="robbery">Robbery</option>
                            <option value="assault">Assault</option>
                            <option value="burglary">Burglary</option>
                            <option value="theft">Theft</option>
                            <option value="vandalism">Vandalism</option>
                            <option value="drug">Drug Related</option>
                        </select>
                    </div>
                    
                    <div class="view-toggles">
                        <button id="toggleHeatmap" class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-fire"></i> Heatmap
                        </button>
                        <button id="toggleClusters" class="btn btn-sm btn-outline-success">
                            <i class="fas fa-layer-group"></i> Clusters
                        </button>
                    </div>
                </div>
            `;
            
            // Prevent map interaction when using controls
            L.DomEvent.disableClickPropagation(div);
            L.DomEvent.disableScrollPropagation(div);
            
            return div;
        };
        
        controlPanel.addTo(this.map);
        
        // Add event listeners for controls
        setTimeout(() => {
            this.setupControlEvents();
        }, 100);
    }
    
    setupControlEvents() {
        // Time filter
        const timeFilter = document.getElementById('timeFilter');
        if (timeFilter) {
            timeFilter.addEventListener('change', (e) => {
                this.currentTimeFilter = e.target.value;
                this.updateMapData();
            });
        }
        
        // Crime type filter
        const crimeFilter = document.getElementById('crimeFilter');
        if (crimeFilter) {
            crimeFilter.addEventListener('change', (e) => {
                this.currentCrimeFilter = e.target.value;
                this.updateMapData();
            });
        }
        
        // Heatmap toggle
        const heatmapToggle = document.getElementById('toggleHeatmap');
        if (heatmapToggle) {
            heatmapToggle.addEventListener('click', () => {
                if (this.map.hasLayer(this.heatmapLayer)) {
                    this.map.removeLayer(this.heatmapLayer);
                    heatmapToggle.classList.remove('active');
                } else {
                    this.map.addLayer(this.heatmapLayer);
                    heatmapToggle.classList.add('active');
                }
            });
        }
        
        // Cluster toggle
        const clusterToggle = document.getElementById('toggleClusters');
        if (clusterToggle) {
            clusterToggle.classList.add('active'); // Default active
            clusterToggle.addEventListener('click', () => {
                if (this.map.hasLayer(this.clusterGroup)) {
                    this.map.removeLayer(this.clusterGroup);
                    clusterToggle.classList.remove('active');
                } else {
                    this.map.addLayer(this.clusterGroup);
                    clusterToggle.classList.add('active');
                }
            });
        }
    }
    
    startRealTimeUpdates() {
        // Simulate real-time updates
        setInterval(() => {
            this.simulateNewIncident();
        }, this.config.updateInterval);
        
        console.log('🔄 Real-time updates started');
    }
    
    simulateNewIncident() {
        // Add a new random incident to simulate real-time data
        const newIncidents = this.generateSampleCrimeData().slice(0, 1);
        newIncidents[0].id = `incident_${Date.now()}`;
        newIncidents[0].date = new Date().toISOString().split('T')[0];
        
        this.crimeData.unshift(newIncidents[0]);
        
        // Keep only last 200 incidents for performance
        if (this.crimeData.length > 200) {
            this.crimeData = this.crimeData.slice(0, 200);
        }
        
        this.updateMapData();
        
        // Show notification for new incident
        this.showNewIncidentNotification(newIncidents[0]);
    }
    
    showNewIncidentNotification(incident) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'crime-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${this.getCrimeIcon(incident.crime_type)}"></i>
                <div>
                    <strong>New ${incident.crime_type} reported</strong>
                    <br><small>${incident.location}</small>
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
    
    showIncidentDetails(incidentId) {
        const incident = this.crimeData.find(i => i.id === incidentId);
        if (!incident) return;
        
        // This would open a detailed modal or sidebar
        console.log('Show details for incident:', incident);
        alert(`Detailed view for ${incident.crime_type} incident at ${incident.location}`);
    }
    
    reportSimilar(incidentId) {
        // This would open a form to report similar incidents
        console.log('Report similar incident:', incidentId);
        alert('Report similar incident functionality would be implemented here');
    }
    
    showError(message) {
        console.error('Map Error:', message);
        // Show user-friendly error message
    }
}

// Global instance for easy access
let advancedMap = null;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const mapContainer = document.getElementById('advanced-crime-map');
    if (mapContainer) {
        advancedMap = new AdvancedCrimeMap('advanced-crime-map');
    }
});

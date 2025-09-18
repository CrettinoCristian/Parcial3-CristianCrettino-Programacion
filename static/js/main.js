// Mini CRM Personal - JavaScript Principal

// Configuración global
const CRM = {
    config: {
        animationDuration: 300,
        debounceDelay: 300,
        autoSaveDelay: 2000
    },
    
    // Utilidades
    utils: {
        // Debounce function para optimizar búsquedas
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        
        // Formatear fechas
        formatDate: function(date) {
            return new Intl.DateTimeFormat('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            }).format(new Date(date));
        },
        
        // Formatear tiempo relativo
        timeAgo: function(date) {
            const now = new Date();
            const past = new Date(date);
            const diffInSeconds = Math.floor((now - past) / 1000);
            
            const intervals = {
                año: 31536000,
                mes: 2592000,
                semana: 604800,
                día: 86400,
                hora: 3600,
                minuto: 60
            };
            
            for (const [unit, seconds] of Object.entries(intervals)) {
                const interval = Math.floor(diffInSeconds / seconds);
                if (interval >= 1) {
                    return `Hace ${interval} ${unit}${interval > 1 ? (unit === 'mes' ? 'es' : 's') : ''}`;
                }
            }
            
            return 'Hace un momento';
        },
        
        // Mostrar notificaciones toast
        showToast: function(message, type = 'info') {
            const toastContainer = document.getElementById('toast-container') || this.createToastContainer();
            
            const toast = document.createElement('div');
            toast.className = `toast align-items-center text-white bg-${type} border-0`;
            toast.setAttribute('role', 'alert');
            toast.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            `;
            
            toastContainer.appendChild(toast);
            
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
            
            // Remover el toast después de que se oculte
            toast.addEventListener('hidden.bs.toast', () => {
                toast.remove();
            });
        },
        
        // Crear contenedor de toasts
        createToastContainer: function() {
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            container.style.zIndex = '1055';
            document.body.appendChild(container);
            return container;
        },
        
        // Copiar al portapapeles
        copyToClipboard: function(text, successMessage = 'Copiado al portapapeles') {
            navigator.clipboard.writeText(text).then(() => {
                this.showToast(successMessage, 'success');
            }).catch(() => {
                this.showToast('Error al copiar', 'danger');
            });
        },
        
        // Validar email
        isValidEmail: function(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        },
        
        // Validar teléfono
        isValidPhone: function(phone) {
            const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
            return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
        }
    },
    
    // Inicialización
    init: function() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupFormValidation();
        this.setupSearch();
        this.setupAutoSave();
        console.log('Mini CRM inicializado correctamente');
    },
    
    // Configurar event listeners globales
    setupEventListeners: function() {
        // Confirmar eliminaciones
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-confirm]')) {
                const message = e.target.getAttribute('data-confirm');
                if (!confirm(message)) {
                    e.preventDefault();
                    return false;
                }
            }
        });
        
        // Copiar al portapapeles
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-copy]')) {
                const text = e.target.getAttribute('data-copy');
                this.utils.copyToClipboard(text);
            }
        });
        
        // Auto-resize de textareas
        document.addEventListener('input', (e) => {
            if (e.target.matches('textarea[data-auto-resize]')) {
                e.target.style.height = 'auto';
                e.target.style.height = e.target.scrollHeight + 'px';
            }
        });
        
        // Animaciones de entrada
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        });
        
        document.querySelectorAll('.card, .alert').forEach(el => {
            observer.observe(el);
        });
    },
    
    // Inicializar componentes
    initializeComponents: function() {
        // Inicializar tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        
        // Inicializar popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
        
        // Actualizar tiempo relativo cada minuto
        this.updateRelativeTimes();
        setInterval(() => this.updateRelativeTimes(), 60000);
    },
    
    // Actualizar tiempos relativos
    updateRelativeTimes: function() {
        document.querySelectorAll('[data-time]').forEach(el => {
            const time = el.getAttribute('data-time');
            el.textContent = this.utils.timeAgo(time);
        });
    },
    
    // Configurar validación de formularios
    setupFormValidation: function() {
        document.querySelectorAll('form:not([action*="login"])').forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                form.classList.add('was-validated');
            });
            
            // Validación en tiempo real
            form.querySelectorAll('input, textarea, select').forEach(field => {
                field.addEventListener('blur', () => {
                    this.validateField(field);
                });
            });
        });
    },
    
    // Validar campo individual
    validateField: function(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';
        
        // Validaciones específicas
        if (field.type === 'email' && value && !this.utils.isValidEmail(value)) {
            isValid = false;
            message = 'Formato de email inválido';
        }
        
        if (field.type === 'tel' && value && !this.utils.isValidPhone(value)) {
            isValid = false;
            message = 'Formato de teléfono inválido';
        }
        
        // Mostrar/ocultar mensaje de error
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = message;
        }
        
        field.classList.toggle('is-invalid', !isValid && value);
        field.classList.toggle('is-valid', isValid && value);
        
        return isValid;
    },
    
    // Configurar búsqueda
    setupSearch: function() {
        const searchInputs = document.querySelectorAll('input[data-search]');
        
        searchInputs.forEach(input => {
            const debouncedSearch = this.utils.debounce((query) => {
                this.performSearch(query, input.getAttribute('data-search'));
            }, this.config.debounceDelay);
            
            input.addEventListener('input', (e) => {
                debouncedSearch(e.target.value);
            });
        });
    },
    
    // Realizar búsqueda
    performSearch: function(query, target) {
        const items = document.querySelectorAll(`[data-searchable="${target}"]`);
        
        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            const matches = text.includes(query.toLowerCase());
            item.style.display = matches ? '' : 'none';
        });
        
        // Mostrar mensaje si no hay resultados
        const visibleItems = Array.from(items).filter(item => item.style.display !== 'none');
        const noResultsMsg = document.querySelector(`[data-no-results="${target}"]`);
        
        if (noResultsMsg) {
            noResultsMsg.style.display = visibleItems.length === 0 ? '' : 'none';
        }
    },
    
    // Configurar auto-guardado
    setupAutoSave: function() {
        const autoSaveForms = document.querySelectorAll('form[data-auto-save]');
        
        autoSaveForms.forEach(form => {
            const debouncedSave = this.utils.debounce(() => {
                this.autoSaveForm(form);
            }, this.config.autoSaveDelay);
            
            form.addEventListener('input', debouncedSave);
        });
    },
    
    // Auto-guardar formulario
    autoSaveForm: function(form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Guardar en localStorage
        const formId = form.id || 'auto-save-form';
        localStorage.setItem(`crm-auto-save-${formId}`, JSON.stringify(data));
        
        // Mostrar indicador de guardado
        this.showSaveIndicator();
    },
    
    // Mostrar indicador de guardado
    showSaveIndicator: function() {
        let indicator = document.getElementById('save-indicator');
        
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'save-indicator';
            indicator.className = 'position-fixed bottom-0 start-0 p-3';
            indicator.style.zIndex = '1050';
            document.body.appendChild(indicator);
        }
        
        indicator.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="bi bi-check-circle"></i> Guardado automáticamente
            </div>
        `;
        
        setTimeout(() => {
            const alert = indicator.querySelector('.alert');
            if (alert) {
                alert.classList.remove('show');
                setTimeout(() => indicator.innerHTML = '', 150);
            }
        }, 2000);
    },
    
    // Restaurar datos del formulario
    restoreFormData: function(formId) {
        const savedData = localStorage.getItem(`crm-auto-save-${formId}`);
        
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                const form = document.getElementById(formId);
                
                if (form) {
                    Object.entries(data).forEach(([name, value]) => {
                        const field = form.querySelector(`[name="${name}"]`);
                        if (field && !field.value) {
                            field.value = value;
                        }
                    });
                }
            } catch (e) {
                console.error('Error restaurando datos del formulario:', e);
            }
        }
    },
    
    // Limpiar datos guardados
    clearSavedData: function(formId) {
        localStorage.removeItem(`crm-auto-save-${formId}`);
    }
};

// Gestor de Modal de Estadísticas
const StatsModalManager = {
    modal: null,
    modalTitle: null,
    modalBody: null,
    closeBtn: null,
    
    init: function() {
        this.modal = document.getElementById('statsModal');
        this.modalTitle = document.getElementById('modalTitle');
        this.modalBody = document.getElementById('modalBody');
        this.closeBtn = document.getElementById('closeModal');
        
        if (!this.modal) return;
        
        this.setupEventListeners();
        this.setupClickableStats();
    },
    
    setupEventListeners: function() {
        // Cerrar modal con botón X
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.closeModal());
        }
        
        // Cerrar modal al hacer clic en el fondo
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });
        
        // Cerrar modal con tecla Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('show')) {
                this.closeModal();
            }
        });
    },
    
    setupClickableStats: function() {
        const clickableSections = document.querySelectorAll('.stats-section-clickable');
        
        clickableSections.forEach(section => {
            section.addEventListener('click', (e) => {
                e.preventDefault();
                const title = section.getAttribute('data-modal-title');
                const contentType = section.getAttribute('data-modal-content');
                this.openModal(title, contentType, section);
            });
            
            // Agregar indicador visual de que es clickeable
            section.style.cursor = 'pointer';
        });
    },
    
    openModal: function(title, contentType, sourceElement) {
        if (!this.modal) return;
        
        // Establecer título
        if (this.modalTitle) {
            this.modalTitle.textContent = title;
        }
        
        // Generar contenido basado en el tipo
        const content = this.generateModalContent(contentType, sourceElement);
        if (this.modalBody) {
            this.modalBody.innerHTML = content;
        }
        
        // Mostrar modal con animación
        this.modal.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevenir scroll del body
        
        // Focus en el botón de cerrar para accesibilidad
        if (this.closeBtn) {
            this.closeBtn.focus();
        }
    },
    
    closeModal: function() {
        if (!this.modal) return;
        
        this.modal.classList.remove('show');
        document.body.style.overflow = ''; // Restaurar scroll del body
    },
    
    generateModalContent: function(contentType, sourceElement) {
        const cardBody = sourceElement.querySelector('.card-body');
        if (!cardBody) return '<p>No hay contenido disponible</p>';
        
        let content = '<div class="stats-content">';
        
        // Buscar imagen del gráfico
        const img = cardBody.querySelector('img');
        if (img) {
            const imageId = 'zoomableImage_' + Date.now();
            content += `
                <div class="zoom-controls">
                    <div class="zoom-buttons">
                        <button class="zoom-btn" onclick="StatsModalManager.zoomOut('${imageId}')">-</button>
                        <button class="zoom-btn" onclick="StatsModalManager.resetZoom('${imageId}')">⌂</button>
                        <button class="zoom-btn" onclick="StatsModalManager.zoomIn('${imageId}')">+</button>
                    </div>
                    <input type="range" 
                           class="zoom-slider" 
                           id="zoomSlider_${imageId}"
                           min="25" 
                           max="500" 
                           value="100" 
                           step="25"
                           oninput="StatsModalManager.setZoom('${imageId}', this.value)">
                    <div class="zoom-level" id="zoomLevel_${imageId}">100%</div>
                </div>
                <div class="image-container" style="overflow: auto; cursor: grab; position: relative;">
                    <img src="${img.src}" 
                         id="${imageId}"
                         class="zoomable-image" 
                         alt="${img.alt}"
                         style="max-width: none; height: auto; transform: scale(1); transition: transform 0.2s ease;"
                         ondblclick="StatsModalManager.toggleZoom('${imageId}')">
                </div>
            `;
        }
        
        // Buscar tabla de datos
        const table = cardBody.querySelector('table');
        if (table) {
            content += `
                <div class="table-responsive mt-4">
                    <h4>Datos Detallados</h4>
                    ${table.outerHTML}
                </div>
            `;
        }
        
        // Buscar métricas adicionales
        const metrics = cardBody.querySelectorAll('.badge, .text-muted, .fw-bold');
        if (metrics.length > 0) {
            content += '<div class="mt-3"><h5>Información Adicional</h5>';
            metrics.forEach(metric => {
                if (metric.textContent.trim()) {
                    content += `<p class="mb-1">${metric.outerHTML}</p>`;
                }
            });
            content += '</div>';
        }
        
        // Agregar información contextual según el tipo
        switch (contentType) {
            case 'etiquetas':
                content += this.getEtiquetasInfo();
                break;
            case 'interacciones':
                content += this.getInteraccionesInfo();
                break;
            case 'empresas':
                content += this.getEmpresasInfo();
                break;
        }
        
        content += '</div>';
        return content;
    },
    
    getEtiquetasInfo: function() {
        return `
            <div class="mt-4 p-3" style="background: rgba(255, 255, 255, 0.05); border: 1px solid #333; border-radius: 8px;">
                <h5 style="color: #3498db;"><i class="bi bi-info-circle"></i> Acerca de las Etiquetas</h5>
                <p class="mb-2" style="color: #bdc3c7;">Las etiquetas te ayudan a categorizar y organizar tus contactos de manera eficiente.</p>
                <ul class="mb-0" style="color: #ecf0f1;">
                    <li>Usa etiquetas descriptivas como "Cliente", "Proveedor", "Prospecto"</li>
                    <li>Puedes asignar múltiples etiquetas a un mismo contacto</li>
                    <li>Filtra contactos por etiquetas desde la lista principal</li>
                </ul>
            </div>
        `;
    },
    
    getInteraccionesInfo: function() {
        return `
            <div class="mt-4 p-3" style="background: rgba(255, 255, 255, 0.05); border: 1px solid #333; border-radius: 8px;">
                <h5 style="color: #3498db;"><i class="bi bi-info-circle"></i> Análisis de Interacciones</h5>
                <p class="mb-2" style="color: #bdc3c7;">Este gráfico muestra la evolución de tus interacciones a lo largo del tiempo.</p>
                <ul class="mb-0" style="color: #ecf0f1;">
                    <li>Identifica patrones en tu actividad de seguimiento</li>
                    <li>Planifica mejor tus futuras interacciones</li>
                    <li>Mantén un registro consistente de comunicaciones</li>
                </ul>
            </div>
        `;
    },
    
    getEmpresasInfo: function() {
        return `
            <div class="mt-4 p-3" style="background: rgba(255, 255, 255, 0.05); border: 1px solid #333; border-radius: 8px;">
                <h5 style="color: #3498db;"><i class="bi bi-info-circle"></i> Distribución por Empresas</h5>
                <p class="mb-2" style="color: #bdc3c7;">Visualiza cómo se distribuyen tus contactos entre diferentes empresas.</p>
                <ul class="mb-0" style="color: #ecf0f1;">
                    <li>Identifica tus principales fuentes de contactos</li>
                    <li>Diversifica tu red de contactos empresariales</li>
                    <li>Enfócate en empresas con mayor potencial</li>
                </ul>
            </div>
        `;
    },
    
    // Funciones de Zoom
    zoomIn: function(imageId) {
        const slider = document.getElementById('zoomSlider_' + imageId);
        if (slider) {
            const currentValue = parseInt(slider.value);
            const newValue = Math.min(500, currentValue + 25);
            slider.value = newValue;
            this.setZoom(imageId, newValue);
        }
    },
    
    zoomOut: function(imageId) {
        const slider = document.getElementById('zoomSlider_' + imageId);
        if (slider) {
            const currentValue = parseInt(slider.value);
            const newValue = Math.max(25, currentValue - 25);
            slider.value = newValue;
            this.setZoom(imageId, newValue);
        }
    },
    
    resetZoom: function(imageId) {
        const slider = document.getElementById('zoomSlider_' + imageId);
        if (slider) {
            slider.value = 100;
            this.setZoom(imageId, 100);
        }
    },
    
    setZoom: function(imageId, zoomLevel) {
        const image = document.getElementById(imageId);
        const zoomDisplay = document.getElementById('zoomLevel_' + imageId);
        const container = image?.parentElement;
        
        if (image) {
            const scale = zoomLevel / 100;
            image.style.transform = `scale(${scale})`;
            image.style.transformOrigin = 'center center';
            
            // Configurar el contenedor para permitir scroll cuando la imagen es más grande
            if (container) {
                container.style.overflow = 'auto';
                container.style.maxHeight = '70vh';
                container.style.maxWidth = '100%';
                container.style.border = '1px solid #444';
                container.style.borderRadius = '8px';
                
                // Habilitar arrastre para desplazamiento
                this.enableDragScroll(container);
            }
        }
        
        if (zoomDisplay) {
            zoomDisplay.textContent = zoomLevel + '%';
        }
    },
    
    toggleZoom: function(imageId) {
        const slider = document.getElementById('zoomSlider_' + imageId);
        if (slider) {
            const currentValue = parseInt(slider.value);
            const newValue = currentValue === 100 ? 200 : 100;
            slider.value = newValue;
            this.setZoom(imageId, newValue);
        }
    },
    
    // Nueva función para habilitar arrastre con mouse
    enableDragScroll: function(container) {
        let isDown = false;
        let startX;
        let startY;
        let scrollLeft;
        let scrollTop;
        
        // Remover listeners previos para evitar duplicados
        container.onmousedown = null;
        container.onmouseleave = null;
        container.onmouseup = null;
        container.onmousemove = null;
        
        container.addEventListener('mousedown', (e) => {
            isDown = true;
            container.style.cursor = 'grabbing';
            startX = e.pageX - container.offsetLeft;
            startY = e.pageY - container.offsetTop;
            scrollLeft = container.scrollLeft;
            scrollTop = container.scrollTop;
            e.preventDefault();
        });
        
        container.addEventListener('mouseleave', () => {
            isDown = false;
            container.style.cursor = 'grab';
        });
        
        container.addEventListener('mouseup', () => {
            isDown = false;
            container.style.cursor = 'grab';
        });
        
        container.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - container.offsetLeft;
            const y = e.pageY - container.offsetTop;
            const walkX = (x - startX) * 2;
            const walkY = (y - startY) * 2;
            container.scrollLeft = scrollLeft - walkX;
            container.scrollTop = scrollTop - walkY;
        });
        
        // Soporte para rueda del mouse para zoom
        container.addEventListener('wheel', (e) => {
            if (e.ctrlKey) {
                e.preventDefault();
                const imageId = container.querySelector('.zoomable-image').id;
                const slider = document.getElementById('zoomSlider_' + imageId);
                if (slider) {
                    const currentValue = parseInt(slider.value);
                    const delta = e.deltaY > 0 ? -25 : 25;
                    const newValue = Math.max(25, Math.min(500, currentValue + delta));
                    slider.value = newValue;
                    this.setZoom(imageId, newValue);
                }
            }
        });
    }
};

// Gestor de Contactos
const ContactosManager = {
    // Agregar etiqueta desde sugerencias
    addTag: function(tag, inputId = 'etiquetas') {
        const input = document.getElementById(inputId);
        if (!input) return;
        
        const currentTags = input.value.trim();
        const tagsArray = currentTags ? currentTags.split(',').map(t => t.trim()) : [];
        
        if (!tagsArray.includes(tag)) {
            const newTags = currentTags ? `${currentTags}, ${tag}` : tag;
            input.value = newTags;
            input.focus();
        }
    },
    
    // Validar formulario de contacto
    validateContactForm: function(form) {
        const nombre = form.querySelector('[name="nombre"]').value.trim();
        const email = form.querySelector('[name="email"]').value.trim();
        
        if (!nombre) {
            CRM.utils.showToast('El nombre es obligatorio', 'danger');
            return false;
        }
        
        if (email && !CRM.utils.isValidEmail(email)) {
            CRM.utils.showToast('El formato del email no es válido', 'danger');
            return false;
        }
        
        return true;
    }
};

// Funciones específicas para interacciones
const InteraccionesManager = {
    // Aplicar plantilla de interacción
    applyTemplate: function(template, textareaId = 'nota') {
        const textarea = document.getElementById(textareaId);
        if (!textarea) return;
        
        const templates = {
            llamada: 'Llamada telefónica\n\nTemas tratados:\n- \n\nAcuerdos:\n- \n\nPróximos pasos:\n- ',
            reunion: 'Reunión presencial\n\nUbicación: \nDuración: \n\nTemas discutidos:\n- \n\nDecisiones tomadas:\n- \n\nAcciones a seguir:\n- ',
            email: 'Intercambio de emails\n\nAsunto: \n\nPuntos principales:\n- \n\nRespuesta requerida:\n- \n\nSeguimiento programado: ',
            seguimiento: 'Seguimiento\n\nMotivo del seguimiento: \n\nEstado actual: \n\nPróximas acciones:\n- \n\nFecha próximo contacto: '
        };
        
        const templateText = templates[template];
        if (!templateText) return;
        
        if (!textarea.value.trim() || confirm('¿Reemplazar el contenido actual?')) {
            textarea.value = templateText;
            textarea.focus();
            
            // Posicionar cursor en el primer campo vacío
            const firstField = templateText.indexOf('- ');
            if (firstField !== -1) {
                textarea.setSelectionRange(firstField + 2, firstField + 2);
            }
        }
    },
    
    // Validar formulario de interacción
    validateInteractionForm: function(form) {
        const nota = form.querySelector('[name="nota"]').value.trim();
        
        if (!nota) {
            CRM.utils.showToast('La descripción es obligatoria', 'danger');
            return false;
        }
        
        if (nota.length < 10) {
            CRM.utils.showToast('La descripción debe tener al menos 10 caracteres', 'danger');
            return false;
        }
        
        return true;
    }
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    CRM.init();
    
    // Inicializar gestor de modal de estadísticas
    StatsModalManager.init();
    
    // Exponer funciones globalmente para uso en templates
    window.CRM = CRM;
    window.ContactosManager = ContactosManager;
    window.InteraccionesManager = InteraccionesManager;
    
    // Funciones de conveniencia globales
    window.agregarEtiqueta = ContactosManager.addTag;
    window.aplicarPlantilla = InteraccionesManager.applyTemplate;
    
    // Mostrar toast de bienvenida si es necesario
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('welcome') === 'true') {
        CRM.utils.showToast('¡Bienvenido a tu Mini CRM Personal!', 'success');
    }
});

// Manejar errores globales
window.addEventListener('error', function(e) {
    console.error('Error en Mini CRM:', e.error);
    CRM.utils.showToast('Ha ocurrido un error inesperado', 'danger');
});

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CRM, ContactosManager, InteraccionesManager };
}
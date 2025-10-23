import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DocumentService, DocumentMedical, DocumentType, UploadDocumentRequest } from '../../services/document.service';

@Component({
  selector: 'app-documents',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './documents.component.html',
  styleUrls: ['./documents.component.css']
})
export class DocumentsComponent implements OnInit {
  documents: DocumentMedical[] = [];
  documentTypes: DocumentType[] = [];
  filteredDocuments: DocumentMedical[] = [];
  
  isLoading = true;
  error = '';
  successMessage = '';
  
  // Modal d'upload
  showUploadModal = false;
  isUploading = false;
  uploadData: any = {
    type_document: '',
    nom_document: '',
    description: '',
    date_document: '',
    medecin_prescripteur: '',
    file: null
  };
  
  // Filtres
  currentFilter = 'all';
  searchTerm = '';

  constructor(private documentService: DocumentService) {}

  ngOnInit() {
    this.loadDocuments();
    this.loadDocumentTypes();
  }

  loadDocuments() {
    this.isLoading = true;
    this.documentService.getDocuments().subscribe({
      next: (response) => {
        this.documents = response.documents.sort((a, b) => 
          new Date(b.date_upload).getTime() - new Date(a.date_upload).getTime()
        );
        this.applyFilters();
        this.isLoading = false;
      },
      error: (error) => {
        this.error = 'Erreur lors du chargement des documents';
        this.isLoading = false;
        console.error('Error loading documents:', error);
      }
    });
  }

  loadDocumentTypes() {
    this.documentService.getDocumentTypes().subscribe({
      next: (response) => {
        this.documentTypes = response.types;
      },
      error: (error) => {
        console.error('Error loading document types:', error);
      }
    });
  }

  applyFilters() {
    let filtered = [...this.documents];
    
    // Filtre par type
    if (this.currentFilter !== 'all') {
      filtered = filtered.filter(doc => doc.type_document === this.currentFilter);
    }
    
    // Filtre par recherche
    if (this.searchTerm.trim()) {
      const term = this.searchTerm.toLowerCase();
      filtered = filtered.filter(doc => 
        doc.nom_document.toLowerCase().includes(term) ||
        doc.description?.toLowerCase().includes(term) ||
        doc.medecin_prescripteur?.toLowerCase().includes(term)
      );
    }
    
    this.filteredDocuments = filtered;
  }

  onFilterChange(filter: string) {
    this.currentFilter = filter;
    this.applyFilters();
  }

  onSearchChange() {
    this.applyFilters();
  }

  openUploadModal() {
    this.uploadData = {
      type_document: '',
      nom_document: '',
      description: '',
      date_document: '',
      medecin_prescripteur: '',
      file: null
    };
    this.showUploadModal = true;
  }

  closeUploadModal() {
    this.showUploadModal = false;
    this.uploadData.file = null;
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      // Vérifier la taille (10MB max)
      if (file.size > 10 * 1024 * 1024) {
        this.error = 'Le fichier est trop volumineux (maximum 10MB)';
        return;
      }
      
      // Vérifier le type
      const allowedTypes = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'];
      const fileExtension = file.name.split('.').pop()?.toLowerCase();
      
      if (!fileExtension || !allowedTypes.includes(fileExtension)) {
        this.error = 'Type de fichier non autorisé. Formats acceptés: PDF, JPG, PNG, DOC, DOCX';
        return;
      }
      
      this.uploadData.file = file;
      
      // Auto-remplir le nom du document si vide
      if (!this.uploadData.nom_document) {
        this.uploadData.nom_document = file.name.split('.')[0];
      }
    }
  }

  uploadDocument() {
    if (!this.uploadData.file || !this.uploadData.type_document || !this.uploadData.nom_document) {
      this.error = 'Veuillez remplir tous les champs obligatoires et sélectionner un fichier';
      return;
    }

    this.isUploading = true;
    this.error = '';

    const uploadRequest: UploadDocumentRequest = {
      type_document: this.uploadData.type_document,
      nom_document: this.uploadData.nom_document,
      description: this.uploadData.description || undefined,
      date_document: this.uploadData.date_document || undefined,
      medecin_prescripteur: this.uploadData.medecin_prescripteur || undefined,
      file: this.uploadData.file
    };

    this.documentService.uploadDocument(uploadRequest).subscribe({
      next: (response) => {
        this.successMessage = 'Document uploadé avec succès';
        this.closeUploadModal();
        this.loadDocuments();
        this.isUploading = false;
        setTimeout(() => this.successMessage = '', 5000);
      },
      error: (error) => {
        this.error = error.error?.error || 'Erreur lors de l\'upload du document';
        this.isUploading = false;
        setTimeout(() => this.error = '', 5000);
      }
    });
  }

  downloadDocument(document: DocumentMedical) {
    this.documentService.downloadDocument(document.id).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = document.nom_fichier;
        link.click();
        window.URL.revokeObjectURL(url);
      },
      error: (error) => {
        this.error = 'Erreur lors du téléchargement du document';
        setTimeout(() => this.error = '', 5000);
      }
    });
  }

  deleteDocument(document: DocumentMedical) {
    if (!confirm(`Êtes-vous sûr de vouloir supprimer le document "${document.nom_document}" ?`)) {
      return;
    }

    this.documentService.deleteDocument(document.id).subscribe({
      next: (response) => {
        this.successMessage = 'Document supprimé avec succès';
        this.loadDocuments();
        setTimeout(() => this.successMessage = '', 5000);
      },
      error: (error) => {
        this.error = 'Erreur lors de la suppression du document';
        setTimeout(() => this.error = '', 5000);
      }
    });
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  }

  formatFileSize(bytes: number): string {
    return this.documentService.formatFileSize(bytes);
  }

  getDocumentTypeLabel(type: string): string {
    return this.documentService.getDocumentTypeLabel(type);
  }

  getDocumentTypeIcon(type: string): string {
    return this.documentService.getDocumentTypeIcon(type);
  }

  getDocumentTypeColor(type: string): string {
    return this.documentService.getDocumentTypeColor(type);
  }

  get documentCounts() {
    return {
      all: this.documents.length,
      analyse: this.documents.filter(doc => doc.type_document === 'analyse').length,
      ordonnance: this.documents.filter(doc => doc.type_document === 'ordonnance').length,
      radio: this.documents.filter(doc => doc.type_document === 'radio').length,
      autre: this.documents.filter(doc => doc.type_document === 'autre').length
    };
  }
}

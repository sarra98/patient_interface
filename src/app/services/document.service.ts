import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DocumentMedical {
  id: number;
  patient_id: number;
  type_document: string;
  nom_document: string;
  description?: string;
  nom_fichier: string;
  taille_fichier: number;
  date_upload: string;
  date_document?: string;
  medecin_prescripteur?: string;
}

export interface DocumentType {
  value: string;
  label: string;
  icon: string;
}

export interface UploadDocumentRequest {
  type_document: string;
  nom_document: string;
  description?: string;
  date_document?: string;
  medecin_prescripteur?: string;
  file: File;
}

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private apiUrl = '/api/documents';

  constructor(private http: HttpClient) {}

  private getHeaders(): { headers: HttpHeaders } {
    const token = localStorage.getItem('token');
    return {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`
      })
    };
  }

  private getMultipartHeaders(): { headers: HttpHeaders } {
    const token = localStorage.getItem('token');
    return {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`
        // Ne pas définir Content-Type pour multipart/form-data
      })
    };
  }

  getDocuments(): Observable<{ documents: DocumentMedical[] }> {
    return this.http.get<{ documents: DocumentMedical[] }>(
      this.apiUrl,
      this.getHeaders()
    );
  }

  getDocumentTypes(): Observable<{ types: DocumentType[] }> {
    return this.http.get<{ types: DocumentType[] }>(
      `${this.apiUrl}/types`,
      this.getHeaders()
    );
  }

  uploadDocument(documentData: UploadDocumentRequest): Observable<{ message: string; document: DocumentMedical }> {
    const formData = new FormData();
    formData.append('file', documentData.file);
    formData.append('type_document', documentData.type_document);
    formData.append('nom_document', documentData.nom_document);
    
    if (documentData.description) {
      formData.append('description', documentData.description);
    }
    if (documentData.date_document) {
      formData.append('date_document', documentData.date_document);
    }
    if (documentData.medecin_prescripteur) {
      formData.append('medecin_prescripteur', documentData.medecin_prescripteur);
    }

    return this.http.post<{ message: string; document: DocumentMedical }>(
      this.apiUrl,
      formData,
      this.getMultipartHeaders()
    );
  }

  downloadDocument(documentId: number): Observable<Blob> {
    return this.http.get(
      `${this.apiUrl}/${documentId}`,
      {
        ...this.getHeaders(),
        responseType: 'blob'
      }
    );
  }

  deleteDocument(documentId: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(
      `${this.apiUrl}/${documentId}`,
      this.getHeaders()
    );
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  getDocumentTypeLabel(type: string): string {
    const types: { [key: string]: string } = {
      'analyse': 'Analyses médicales',
      'ordonnance': 'Ordonnances',
      'radio': 'Radiographies',
      'autre': 'Autres documents'
    };
    return types[type] || type;
  }

  getDocumentTypeIcon(type: string): string {
    const icons: { [key: string]: string } = {
      'analyse': 'fas fa-vial',
      'ordonnance': 'fas fa-prescription-bottle-alt',
      'radio': 'fas fa-x-ray',
      'autre': 'fas fa-file-medical'
    };
    return icons[type] || 'fas fa-file';
  }

  getDocumentTypeColor(type: string): string {
    const colors: { [key: string]: string } = {
      'analyse': 'primary',
      'ordonnance': 'success',
      'radio': 'warning',
      'autre': 'info'
    };
    return colors[type] || 'secondary';
  }
}

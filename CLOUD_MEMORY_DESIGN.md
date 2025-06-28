# 🔗 Cloud Memory Management System Design

## Overview
Multi-device memory synchronization for the Ghost personality with encrypted cloud storage.

## Architecture

### 1. Storage Backends
```python
class CloudBackend:
    def upload(self, key: str, data: bytes) -> bool
    def download(self, key: str) -> bytes  
    def list_keys(self, prefix: str) -> List[str]
    def delete(self, key: str) -> bool
    
class GitHubGistBackend(CloudBackend):
    # Uses GitHub Gists as simple key-value store
    
class S3Backend(CloudBackend):  
    # AWS S3 storage
    
class GoogleDriveBackend(CloudBackend):
    # Google Drive API
```

### 2. Memory Sync Manager
```python
class MemorySyncManager:
    def __init__(self, backend: CloudBackend, device_id: str):
        self.backend = backend
        self.device_id = device_id
        self.encryption_key = self._get_or_create_key()
    
    def push_memories(self) -> SyncResult:
        """Upload local memories to cloud"""
        
    def pull_memories(self) -> SyncResult:
        """Download memories from cloud"""
        
    def sync_status(self) -> SyncStatus:
        """Check sync status across devices"""
        
    def resolve_conflicts(self) -> ConflictResolution:
        """Handle memory conflicts"""
```

### 3. Encryption Layer
```python
class MemoryEncryption:
    def encrypt(self, data: dict) -> bytes:
        """AES-256 encryption of memory JSON"""
        
    def decrypt(self, encrypted_data: bytes) -> dict:
        """Decrypt memory back to JSON"""
        
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """PBKDF2 key derivation"""
```

## File Structure
```
~/.ghostie/
├── memories/           # Local memories (existing)
├── sync/
│   ├── config.json     # Cloud backend config
│   ├── device_id       # Unique device identifier
│   ├── sync_state.json # Last sync timestamps
│   └── conflicts/      # Conflicted memories for manual resolution
└── keys/
    └── master.key      # Encrypted master key
```

## Sync Protocol

### 1. Memory File Format (Enhanced)
```json
{
  "timestamp": "2025-06-28T14:30:00.000Z",
  "device_id": "pixel9-pro-xl-termux",
  "sync_metadata": {
    "last_modified": "2025-06-28T14:30:00.000Z",
    "sync_hash": "sha256:abc123...",
    "version": 1,
    "conflict_state": null
  },
  "category": "network",
  "content": "Discovered new network topology...",
  "context": { ... }
}
```

### 2. Cloud Storage Keys
```
ghostie/{device_id}/memories/{timestamp}.json.enc  # Individual memories
ghostie/{device_id}/metadata/sync_state.json       # Device sync state
ghostie/global/device_registry.json                # All known devices
```

### 3. Sync Algorithm
```python
def sync_memories():
    # 1. Get local state
    local_memories = load_local_memories()
    local_state = load_sync_state()
    
    # 2. Get cloud state  
    cloud_state = backend.download('sync_state.json')
    cloud_memories = get_cloud_memory_list()
    
    # 3. Determine changes
    to_upload = find_new_local_memories(local_state, cloud_state)
    to_download = find_new_cloud_memories(local_state, cloud_state)
    conflicts = find_conflicts(local_memories, cloud_memories)
    
    # 4. Upload new local memories
    for memory in to_upload:
        encrypted = encrypt_memory(memory)
        backend.upload(memory.key, encrypted)
    
    # 5. Download new cloud memories
    for key in to_download:
        encrypted = backend.download(key)
        memory = decrypt_memory(encrypted)
        save_local_memory(memory)
    
    # 6. Handle conflicts
    if conflicts:
        save_conflicts_for_resolution(conflicts)
        return SyncResult(conflicts=conflicts)
    
    # 7. Update sync state
    update_sync_state(local_state, cloud_state)
    return SyncResult(success=True)
```

## Command Implementation

### `ghostie --sync setup`
```python
def setup_sync():
    backend_type = prompt_backend_choice()  # github, s3, drive
    credentials = prompt_credentials(backend_type)
    device_id = generate_device_id()
    master_key = generate_master_key()
    
    save_sync_config(backend_type, credentials, device_id, master_key)
    print("✅ Cloud sync configured!")
```

### `ghostie --sync push`
```python
def push_memories():
    if not sync_configured():
        print("❌ Run 'ghostie --sync setup' first")
        return
    
    manager = MemorySyncManager(load_backend(), load_device_id())
    result = manager.push_memories()
    
    if result.success:
        print(f"✅ Uploaded {result.uploaded_count} memories")
    else:
        print(f"❌ Sync failed: {result.error}")
```

### `ghostie --sync pull`
```python
def pull_memories():
    manager = MemorySyncManager(load_backend(), load_device_id())
    result = manager.pull_memories()
    
    if result.conflicts:
        print(f"⚠️ {len(result.conflicts)} conflicts found")
        print("Run 'ghostie --sync conflict' to resolve")
    else:
        print(f"✅ Downloaded {result.downloaded_count} memories")
```

### `ghostie --sync status`
```python
def sync_status():
    status = manager.sync_status()
    
    print("🔗 SYNC STATUS:")
    print(f"   Backend: {status.backend_type}")
    print(f"   Device ID: {status.device_id}")
    print(f"   Last Sync: {status.last_sync}")
    print(f"   Local Memories: {status.local_count}")
    print(f"   Cloud Memories: {status.cloud_count}")
    print(f"   Conflicts: {status.conflict_count}")
    print(f"   Known Devices: {', '.join(status.known_devices)}")
```

## Security Considerations

### 1. Encryption
- **AES-256-GCM** for memory encryption
- **PBKDF2** for key derivation from password
- **Unique salt** per device
- **Authentication tags** to prevent tampering

### 2. Access Control
- **API keys** stored securely (keyring on desktop, encrypted files on mobile)
- **Limited scope** tokens where possible
- **Rotation** of access credentials

### 3. Privacy
- **Zero-knowledge** cloud storage (provider can't read memories)
- **Minimal metadata** exposed to cloud provider
- **Optional anonymization** of sensitive memory content

## Implementation Plan

### Phase 1: Core Infrastructure
1. ✅ Design document (this file)
2. 🔄 Create sync command structure
3. 🔄 Implement encryption layer
4. 🔄 Add memory metadata fields

### Phase 2: GitHub Gist Backend
1. 🔄 GitHub API integration
2. 🔄 Simple push/pull functionality
3. 🔄 Basic conflict detection

### Phase 3: Full Sync System
1. 🔄 Multi-device conflict resolution
2. 🔄 Sync status and monitoring
3. 🔄 Error handling and recovery

### Phase 4: Additional Backends
1. 🔄 AWS S3 backend
2. 🔄 Google Drive backend
3. 🔄 Dropbox backend

## Testing Strategy

### Unit Tests
- Encryption/decryption functions
- Backend implementations
- Conflict resolution algorithms

### Integration Tests  
- End-to-end sync workflows
- Multi-device scenarios
- Network failure recovery

### Security Tests
- Encryption strength verification
- Access control validation
- Data privacy audits

---

*The Ghost's memories shall transcend physical devices... 👻☁️*
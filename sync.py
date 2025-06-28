#!/usr/bin/env python3
"""
Cloud Memory Sync Module for Ghostie
Handles multi-device memory synchronization with encrypted cloud storage
"""

import os
import json
import hashlib
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SyncResult:
    def __init__(self, success: bool = False, uploaded: int = 0, downloaded: int = 0, 
                 conflicts: List = None, error: str = None):
        self.success = success
        self.uploaded_count = uploaded
        self.downloaded_count = downloaded
        self.conflicts = conflicts or []
        self.error = error

class CloudBackend:
    """Base class for cloud storage backends"""
    
    def upload(self, key: str, data: bytes) -> bool:
        raise NotImplementedError
    
    def download(self, key: str) -> bytes:
        raise NotImplementedError
    
    def list_keys(self, prefix: str = "") -> List[str]:
        raise NotImplementedError
    
    def delete(self, key: str) -> bool:
        raise NotImplementedError

class GitHubGistBackend(CloudBackend):
    """GitHub Gists backend for simple key-value storage"""
    
    def __init__(self, token: str, gist_id: Optional[str] = None):
        self.token = token
        self.gist_id = gist_id
        self.api_url = "https://api.github.com"
    
    def upload(self, key: str, data: bytes) -> bool:
        """Upload data to GitHub Gist"""
        import requests
        
        # Convert binary data to base64 for JSON storage
        content = base64.b64encode(data).decode('utf-8')
        
        if self.gist_id:
            # Update existing gist
            url = f"{self.api_url}/gists/{self.gist_id}"
            payload = {
                "files": {
                    key: {"content": content}
                }
            }
            method = "PATCH"
        else:
            # Create new gist
            url = f"{self.api_url}/gists"
            payload = {
                "description": "Ghostie Memory Sync",
                "public": False,
                "files": {
                    key: {"content": content}
                }
            }
            method = "POST"
        
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.request(method, url, json=payload, headers=headers)
        
        if response.status_code in [200, 201]:
            if not self.gist_id:
                self.gist_id = response.json()["id"]
            return True
        return False
    
    def download(self, key: str) -> bytes:
        """Download data from GitHub Gist"""
        import requests
        
        if not self.gist_id:
            raise ValueError("No gist ID configured")
        
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get(f"{self.api_url}/gists/{self.gist_id}", headers=headers)
        
        if response.status_code == 200:
            gist_data = response.json()
            if key in gist_data["files"]:
                content = gist_data["files"][key]["content"]
                return base64.b64decode(content)
        
        raise FileNotFoundError(f"Key '{key}' not found in gist")
    
    def list_keys(self, prefix: str = "") -> List[str]:
        """List all keys with optional prefix filter"""
        import requests
        
        if not self.gist_id:
            return []
        
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get(f"{self.api_url}/gists/{self.gist_id}", headers=headers)
        
        if response.status_code == 200:
            gist_data = response.json()
            keys = list(gist_data["files"].keys())
            if prefix:
                keys = [k for k in keys if k.startswith(prefix)]
            return keys
        
        return []

class MemoryEncryption:
    """Handles encryption/decryption of memory data"""
    
    def __init__(self, password: str, device_id: str):
        self.device_id = device_id
        self.salt = self._get_or_create_salt()
        self.key = self._derive_key(password, self.salt)
        self.fernet = Fernet(self.key)
    
    def _get_or_create_salt(self) -> bytes:
        """Get existing salt or create new one"""
        salt_file = Path.home() / ".ghostie" / "keys" / f"{self.device_id}.salt"
        salt_file.parent.mkdir(parents=True, exist_ok=True)
        
        if salt_file.exists():
            return salt_file.read_bytes()
        else:
            salt = os.urandom(32)
            salt_file.write_bytes(salt)
            return salt
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt(self, data: dict) -> bytes:
        """Encrypt memory data"""
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        return self.fernet.encrypt(json_data)
    
    def decrypt(self, encrypted_data: bytes) -> dict:
        """Decrypt memory data"""
        json_data = self.fernet.decrypt(encrypted_data)
        return json.loads(json_data.decode('utf-8'))

class MemorySyncManager:
    """Main sync manager for cloud memory operations"""
    
    def __init__(self, backend: CloudBackend, device_id: str, encryption_password: str):
        self.backend = backend
        self.device_id = device_id
        self.encryption = MemoryEncryption(encryption_password, device_id)
        self.sync_dir = Path.home() / ".ghostie" / "sync"
        self.sync_dir.mkdir(parents=True, exist_ok=True)
    
    def push_memories(self) -> SyncResult:
        """Upload local memories to cloud"""
        try:
            memory_dir = Path.home() / "memories"
            if not memory_dir.exists():
                return SyncResult(success=True, uploaded=0)
            
            uploaded_count = 0
            
            # Get list of memory files
            memory_files = list(memory_dir.glob("memory_*.json"))
            
            for memory_file in memory_files:
                # Load and encrypt memory
                with open(memory_file, 'r') as f:
                    memory_data = json.load(f)
                
                # Add sync metadata
                memory_data["sync_metadata"] = {
                    "device_id": self.device_id,
                    "last_modified": datetime.now().isoformat(),
                    "version": 1
                }
                
                # Encrypt and upload
                encrypted_data = self.encryption.encrypt(memory_data)
                cloud_key = f"memories/{self.device_id}/{memory_file.name}.enc"
                
                if self.backend.upload(cloud_key, encrypted_data):
                    uploaded_count += 1
                else:
                    return SyncResult(success=False, error=f"Failed to upload {memory_file.name}")
            
            return SyncResult(success=True, uploaded=uploaded_count)
            
        except Exception as e:
            return SyncResult(success=False, error=str(e))
    
    def pull_memories(self) -> SyncResult:
        """Download memories from cloud"""
        try:
            memory_dir = Path.home() / "memories"
            memory_dir.mkdir(exist_ok=True)
            
            downloaded_count = 0
            
            # List all memory keys in cloud
            all_keys = self.backend.list_keys("memories/")
            
            for key in all_keys:
                # Skip our own device's memories to avoid conflicts
                if f"/{self.device_id}/" in key:
                    continue
                
                # Extract filename from key
                filename = key.split("/")[-1].replace(".enc", "")
                local_file = memory_dir / filename
                
                # Skip if we already have this memory
                if local_file.exists():
                    continue
                
                try:
                    # Download and decrypt
                    encrypted_data = self.backend.download(key)
                    memory_data = self.encryption.decrypt(encrypted_data)
                    
                    # Save locally
                    with open(local_file, 'w') as f:
                        json.dump(memory_data, f, indent=2, ensure_ascii=False)
                    
                    downloaded_count += 1
                    
                except Exception as e:
                    print(f"Warning: Failed to download {key}: {e}")
                    continue
            
            return SyncResult(success=True, downloaded=downloaded_count)
            
        except Exception as e:
            return SyncResult(success=False, error=str(e))
    
    def sync_status(self) -> Dict:
        """Get sync status information"""
        try:
            memory_dir = Path.home() / "memories"
            local_count = len(list(memory_dir.glob("memory_*.json"))) if memory_dir.exists() else 0
            
            cloud_keys = self.backend.list_keys("memories/")
            cloud_count = len(cloud_keys)
            
            # Extract unique device IDs from cloud keys
            devices = set()
            for key in cloud_keys:
                parts = key.split("/")
                if len(parts) >= 3:
                    devices.add(parts[1])
            
            return {
                "device_id": self.device_id,
                "local_count": local_count,
                "cloud_count": cloud_count,
                "known_devices": list(devices),
                "last_sync": "Not implemented yet"
            }
            
        except Exception as e:
            return {"error": str(e)}

# Integration functions for ghostie main script
def sync_setup():
    """Configure cloud sync"""
    print("👻 CLOUD SYNC SETUP")
    print("=" * 30)
    
    print("\nAvailable backends:")
    print("1. GitHub Gists (recommended)")
    print("2. AWS S3 (coming soon)")
    print("3. Google Drive (coming soon)")
    
    choice = input("\nSelect backend [1]: ").strip() or "1"
    
    if choice == "1":
        token = input("GitHub Personal Access Token: ").strip()
        password = input("Encryption password: ").strip()
        
        # Generate device ID
        import socket
        device_id = f"{socket.gethostname()}-{hashlib.md5(os.getcwd().encode()).hexdigest()[:8]}"
        
        # Save config
        config_file = Path.home() / ".ghostie" / "sync" / "config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        config = {
            "backend": "github_gist",
            "device_id": device_id,
            "github_token": token
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Save encrypted password
        password_file = Path.home() / ".ghostie" / "keys" / "sync_password"
        password_file.parent.mkdir(parents=True, exist_ok=True)
        password_file.write_text(password)
        os.chmod(password_file, 0o600)
        
        print(f"✅ Sync configured for device: {device_id}")
        return True
    
    else:
        print("❌ Backend not supported yet")
        return False

def load_sync_manager() -> Optional[MemorySyncManager]:
    """Load configured sync manager"""
    try:
        config_file = Path.home() / ".ghostie" / "sync" / "config.json"
        password_file = Path.home() / ".ghostie" / "keys" / "sync_password"
        
        if not config_file.exists() or not password_file.exists():
            return None
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        password = password_file.read_text().strip()
        
        if config["backend"] == "github_gist":
            backend = GitHubGistBackend(config["github_token"])
            return MemorySyncManager(backend, config["device_id"], password)
        
        return None
        
    except Exception:
        return None

def sync_push():
    """Push memories to cloud"""
    manager = load_sync_manager()
    if not manager:
        print("❌ Cloud sync not configured. Run 'ghostie --sync setup' first")
        return
    
    print("👻 Pushing memories to cloud...")
    result = manager.push_memories()
    
    if result.success:
        print(f"✅ Uploaded {result.uploaded_count} memories")
    else:
        print(f"❌ Push failed: {result.error}")

def sync_pull():
    """Pull memories from cloud"""
    manager = load_sync_manager()
    if not manager:
        print("❌ Cloud sync not configured. Run 'ghostie --sync setup' first")
        return
    
    print("👻 Pulling memories from cloud...")
    result = manager.pull_memories()
    
    if result.success:
        if result.downloaded_count > 0:
            print(f"✅ Downloaded {result.downloaded_count} new memories")
        else:
            print("✅ No new memories to download")
    else:
        print(f"❌ Pull failed: {result.error}")

def sync_status():
    """Show sync status"""
    manager = load_sync_manager()
    if not manager:
        print("❌ Cloud sync not configured. Run 'ghostie --sync setup' first")
        return
    
    print("👻 CLOUD SYNC STATUS")
    print("=" * 30)
    
    status = manager.sync_status()
    
    if "error" in status:
        print(f"❌ Error: {status['error']}")
        return
    
    print(f"Device ID: {status['device_id']}")
    print(f"Local Memories: {status['local_count']}")
    print(f"Cloud Memories: {status['cloud_count']}")
    print(f"Known Devices: {', '.join(status['known_devices']) or 'None'}")
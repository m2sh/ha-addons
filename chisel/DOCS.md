# Chisel Add-on Documentation

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage Examples](#usage-examples)
5. [Advanced Configuration](#advanced-configuration)
6. [Troubleshooting](#troubleshooting)
7. [Security Considerations](#security-considerations)
8. [API Reference](#api-reference)

## Overview

Chisel is a fast TCP/UDP tunnel, transported over HTTP, secured via SSH. This add-on provides a secure way to tunnel your Home Assistant instance through firewalls and NAT without opening any ports.

### Key Features

- **Dual Mode Operation**: Run as either a server or client
- **SSH-based Security**: All connections are encrypted using SSH protocol
- **Firewall Traversal**: Pass through firewalls and NAT without port forwarding
- **SOCKS5 Support**: Optional SOCKS5 proxy functionality
- **Reverse Tunneling**: Support for reverse port forwarding
- **Authentication**: User authentication with config files
- **TLS Support**: Full TLS/SSL support for secure connections
- **Auto-reconnection**: Client automatically reconnects with exponential backoff

## Installation

### Prerequisites

- Home Assistant OS or Supervised installation
- Supervisor with add-on store access
- Network access to download the Chisel binary

### Installation Steps

1. Open Home Assistant
2. Go to **Settings** → **Add-ons** → **Add-on Store**
3. Search for "Chisel"
4. Click on the Chisel add-on
5. Click **Install**
6. Wait for the installation to complete

## Configuration

### Basic Configuration

The add-on supports two main modes: `server` and `client`. You must choose one mode and configure it appropriately.

#### Server Mode Configuration

```yaml
mode: "server"
server_port: 8080
server_socks5: false
server_reverse: false
log_level: "info"
verbose: false
```

#### Client Mode Configuration

```yaml
mode: "client"
client_server: "https://your-server.com:8080"
client_fingerprint: "your-server-fingerprint"
client_remotes:
  - "8080:localhost:8123"
log_level: "info"
verbose: false
```

### Configuration Options

#### Common Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | string | `"server"` | Operation mode (`server` or `client`) |
| `log_level` | string | `"info"` | Log level (trace, debug, info, notice, warning, error, fatal) |
| `verbose` | boolean | `false` | Enable verbose logging |
| `pid` | boolean | `false` | Generate PID file |

#### Server Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `server_port` | integer | `8080` | Port to listen on |
| `server_keyfile` | string | `""` | Path to server key file |
| `server_authfile` | string | `""` | Path to authentication file |
| `server_socks5` | boolean | `false` | Enable SOCKS5 proxy |
| `server_reverse` | boolean | `false` | Enable reverse tunneling |
| `server_proxy` | string | `""` | Proxy server URL |
| `server_header` | list | `[]` | Custom HTTP headers |

#### Client Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `client_server` | string | `""` | Chisel server URL |
| `client_fingerprint` | string | `""` | Server fingerprint |
| `client_auth` | string | `""` | Authentication credentials |
| `client_remotes` | list | `[]` | Remote tunnel specifications |
| `client_keepalive` | string | `"25s"` | Keepalive interval |
| `client_max_retry_count` | integer | `0` | Maximum retry count |
| `client_max_retry_interval` | string | `"5m"` | Maximum retry interval |
| `client_proxy` | string | `""` | Proxy server URL |
| `client_header` | list | `[]` | Custom HTTP headers |
| `client_hostname` | string | `""` | Custom Host header |
| `client_sni` | string | `""` | Server Name Indication |
| `client_tls_ca` | string | `""` | TLS CA certificate path |
| `client_tls_skip_verify` | boolean | `false` | Skip TLS verification |
| `client_tls_key` | string | `""` | TLS client key path |
| `client_tls_cert` | string | `""` | TLS client certificate path |

## Usage Examples

### Example 1: Basic Server Setup

Create a simple Chisel server:

```yaml
mode: "server"
server_port: 8080
server_socks5: true
log_level: "info"
```

This creates a server that:
- Listens on port 8080
- Provides a SOCKS5 proxy on port 1080
- Logs at info level

### Example 2: Server with Authentication

Create a server with user authentication:

```yaml
mode: "server"
server_port: 8080
server_authfile: "/data/users.json"
server_keyfile: "/data/chisel.key"
log_level: "info"
```

Create the authentication file `/data/users.json`:

```json
{
  "user1": "password1",
  "user2": "password2"
}
```

### Example 3: Client Connecting to Remote Server

Connect to a remote Chisel server:

```yaml
mode: "client"
client_server: "https://your-server.com:8080"
client_fingerprint: "your-server-fingerprint"
client_auth: "username:password"
client_remotes:
  - "8080:localhost:8123"
  - "socks"
client_keepalive: "30s"
```

This configuration:
- Connects to a remote server
- Creates a tunnel from remote port 8080 to local Home Assistant (port 8123)
- Provides a SOCKS5 proxy on the remote server
- Uses authentication
- Verifies server fingerprint

### Example 4: Reverse Tunneling

Set up reverse tunneling:

**Server Configuration:**
```yaml
mode: "server"
server_port: 8080
server_reverse: true
server_authfile: "/data/users.json"
```

**Client Configuration:**
```yaml
mode: "client"
client_server: "https://your-server.com:8080"
client_auth: "username:password"
client_remotes:
  - "R:8080:localhost:8123"
client_fingerprint: "your-server-fingerprint"
```

This creates a reverse tunnel where:
- The server accepts reverse connections
- The client creates a reverse tunnel
- Connections go through the server and out the client

### Example 5: TLS/SSL Configuration

Use TLS for additional security:

```yaml
mode: "client"
client_server: "https://your-server.com:8080"
client_fingerprint: "your-server-fingerprint"
client_tls_ca: "/data/ca.crt"
client_tls_cert: "/data/client.crt"
client_tls_key: "/data/client.key"
client_remotes:
  - "8080:localhost:8123"
```

### Example 6: Custom Headers

Add custom HTTP headers:

```yaml
mode: "server"
server_port: 8080
server_header:
  - "X-Custom-Header: value1"
  - "Authorization: Bearer token123"
```

## Advanced Configuration

### Key Management

#### Generating Server Keys

You can generate a server key using the Chisel command line:

```bash
chisel server --keygen /path/to/keyfile
```

Or let the add-on generate it automatically by specifying a keyfile path in the configuration.

#### Fingerprint Verification

To get the server fingerprint, run the server and look for the fingerprint in the logs:

```
2024/01/01 12:00:00 server: Fingerprint: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=
```

Use this fingerprint in client configurations for security.

### Authentication

#### Server Authentication

Create a JSON file with username/password pairs:

```json
{
  "user1": "password1",
  "user2": "password2"
}
```

#### Client Authentication

Use the format `username:password` in the `client_auth` option.

### Remote Specifications

Remote specifications follow the format: `[R:]local-host:local-port:remote-host:remote-port`

Examples:
- `8080:localhost:8123` - Forward remote port 8080 to local port 8123
- `R:8080:localhost:8123` - Reverse tunnel from server port 8080 to client port 8123
- `socks` - Create a SOCKS5 proxy on the server
- `R:socks` - Create a reverse SOCKS5 proxy

## Troubleshooting

### Common Issues

#### Connection Refused

**Problem**: Client cannot connect to server
**Solutions**:
- Check if server is running
- Verify server URL and port
- Check firewall settings
- Ensure server is accessible from client network

#### Authentication Failed

**Problem**: Authentication errors
**Solutions**:
- Verify username/password
- Check auth file format
- Ensure auth file is readable
- Check file permissions

#### Fingerprint Mismatch

**Problem**: Fingerprint verification fails
**Solutions**:
- Get correct fingerprint from server logs
- Update client configuration
- Check for server key changes

#### Port Already in Use

**Problem**: Server cannot bind to port
**Solutions**:
- Change server port
- Stop conflicting services
- Check port availability

### Log Analysis

#### Server Logs

Look for these log entries:
- `server: Listening on :8080` - Server started successfully
- `server: Fingerprint: xxx=` - Server fingerprint
- `server: session#1: client connected` - Client connected
- `server: session#1: client disconnected` - Client disconnected

#### Client Logs

Look for these log entries:
- `client: Connecting to wss://server:8080` - Connecting to server
- `client: Connected (Latency 50ms)` - Successfully connected
- `client: Fingerprint matched` - Fingerprint verification passed
- `client: Reconnecting...` - Reconnection attempt

### Debug Mode

Enable verbose logging for detailed debugging:

```yaml
verbose: true
log_level: "debug"
```

## Security Considerations

### Best Practices

1. **Always use fingerprint verification** to prevent man-in-the-middle attacks
2. **Use strong authentication** with complex passwords
3. **Enable TLS** when possible for additional encryption
4. **Limit network access** to Chisel ports
5. **Regularly update** the Chisel binary
6. **Monitor logs** for suspicious activity
7. **Use reverse tunnels** when appropriate for additional security

### Network Security

- Chisel uses SSH encryption for all connections
- TLS can be used for transport layer security
- Authentication prevents unauthorized access
- Fingerprint verification ensures server identity

### Key Management

- Store keys securely
- Use strong key generation
- Rotate keys regularly
- Protect key files with appropriate permissions

## API Reference

### Configuration Schema

The add-on uses a YAML configuration schema with the following structure:

```yaml
mode: string  # "server" or "client"
# Server options (when mode = "server")
server_port: integer
server_keyfile: string
server_authfile: string
server_socks5: boolean
server_reverse: boolean
server_proxy: string
server_header: [string]
# Client options (when mode = "client")
client_server: string
client_fingerprint: string
client_auth: string
client_remotes: [string]
client_keepalive: string
client_max_retry_count: integer
client_max_retry_interval: string
client_proxy: string
client_header: [string]
client_hostname: string
client_sni: string
client_tls_ca: string
client_tls_skip_verify: boolean
client_tls_key: string
client_tls_cert: string
# Common options
log_level: string
verbose: boolean
pid: boolean
```

### Environment Variables

The add-on respects the following environment variables:
- `AUTH` - Default authentication credentials (client mode)
- `CHISEL_LOG` - Default log level

### File Paths

Important file paths in the add-on:
- `/data/` - Persistent data directory
- `/usr/bin/chisel` - Chisel binary location
- `/etc/s6-overlay/scripts/` - Configuration scripts

### Ports

Default ports used by the add-on:
- `8080/tcp` - Default server port
- `1080/tcp` - SOCKS5 proxy port (when enabled)

## Support

For additional support:

1. Check the [Home Assistant Community Forum](https://community.home-assistant.io/)
2. Join the [Home Assistant Discord](https://discord.gg/c5DvZ4e)
3. Open an issue on the [GitHub repository](https://github.com/m2sh/ha-addon-chisel/issues)
4. Review the [Chisel documentation](https://github.com/jpillora/chisel)

## Changelog

### Version 1.0.0
- Initial release
- Support for server and client modes
- SSH-based encryption
- SOCKS5 proxy support
- Reverse tunneling
- Authentication support
- TLS/SSL support
- Auto-reconnection
- Multiple architecture support 
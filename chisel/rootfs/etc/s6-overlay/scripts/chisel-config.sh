#!/command/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: Chisel
#
# Configures the Chisel tunnel based on the add-on configuration
# ==============================================================================

# ------------------------------------------------------------------------------
# Checks if the config is valid
# ------------------------------------------------------------------------------
checkConfig() {
    bashio::log.trace "${FUNCNAME[0]}"
    bashio::log.info "Checking add-on config..."

    local mode
    mode=$(bashio::config 'mode')

    # Check if mode is valid
    if [[ "${mode}" != "server" && "${mode}" != "client" ]]; then
        bashio::exit.nok "Invalid mode: ${mode}. Must be either 'server' or 'client'"
    fi

    # Check server-specific configuration
    if [[ "${mode}" == "server" ]]; then
        bashio::log.info "Validating server configuration..."
        
        # Check if port is valid
        if bashio::config.has_value 'server_port' ; then
            local port
            port=$(bashio::config 'server_port')
            if ! [[ "${port}" =~ ^[0-9]+$ ]] || [ "${port}" -lt 1 ] || [ "${port}" -gt 65535 ]; then
                bashio::exit.nok "Invalid server_port: ${port}. Must be a number between 1 and 65535"
            fi
        fi
        
        # Check if keyfile exists if specified
        if bashio::config.has_value 'server_keyfile' ; then
            local keyfile
            keyfile=$(bashio::config 'server_keyfile')
            if [ ! -f "${keyfile}" ]; then
                bashio::exit.nok "Keyfile not found: ${keyfile}"
            fi
        fi
        
        # Check if authfile exists if specified
        if bashio::config.has_value 'server_authfile' ; then
            local authfile
            authfile=$(bashio::config 'server_authfile')
            if [ ! -f "${authfile}" ]; then
                bashio::exit.nok "Authfile not found: ${authfile}"
            fi
        fi

    # Check client-specific configuration
    elif [[ "${mode}" == "client" ]]; then
        bashio::log.info "Validating client configuration..."
        
        # Check if server URL is provided
        if ! bashio::config.has_value 'client_server' ; then
            bashio::exit.nok "client_server is required when running in client mode"
        fi
        
        # Check if remotes are provided
        if ! bashio::config.has_value 'client_remotes' ; then
            bashio::exit.nok "client_remotes is required when running in client mode"
        fi
        
        # Validate keepalive format if provided
        if bashio::config.has_value 'client_keepalive' ; then
            local keepalive
            keepalive=$(bashio::config 'client_keepalive')
            if ! [[ "${keepalive}" =~ ^[0-9]+[smhd]$ ]]; then
                bashio::exit.nok "Invalid keepalive format: ${keepalive}. Must be in format like '25s', '2m', '1h', '1d'"
            fi
        fi
        
        # Validate max retry interval format if provided
        if bashio::config.has_value 'client_max_retry_interval' ; then
            local retry_interval
            retry_interval=$(bashio::config 'client_max_retry_interval')
            if ! [[ "${retry_interval}" =~ ^[0-9]+[smhd]$ ]]; then
                bashio::exit.nok "Invalid max_retry_interval format: ${retry_interval}. Must be in format like '5m', '1h', '1d'"
            fi
        fi
        
        # Check if TLS files exist if specified
        if bashio::config.has_value 'client_tls_key' ; then
            local tls_key
            tls_key=$(bashio::config 'client_tls_key')
            if [ ! -f "${tls_key}" ]; then
                bashio::exit.nok "TLS key file not found: ${tls_key}"
            fi
        fi
        
        if bashio::config.has_value 'client_tls_cert' ; then
            local tls_cert
            tls_cert=$(bashio::config 'client_tls_cert')
            if [ ! -f "${tls_cert}" ]; then
                bashio::exit.nok "TLS certificate file not found: ${tls_cert}"
            fi
        fi
        
        if bashio::config.has_value 'client_tls_ca' ; then
            local tls_ca
            tls_ca=$(bashio::config 'client_tls_ca')
            if [ ! -f "${tls_ca}" ]; then
                bashio::exit.nok "TLS CA file not found: ${tls_ca}"
            fi
        fi
    fi

    bashio::log.info "Configuration validation passed"
}

# ------------------------------------------------------------------------------
# Generate server key if needed
# ------------------------------------------------------------------------------
generateServerKey() {
    bashio::log.trace "${FUNCNAME[0]}"
    
    local mode
    mode=$(bashio::config 'mode')
    
    if [[ "${mode}" == "server" ]]; then
        # Check if keyfile is specified but doesn't exist
        if bashio::config.has_value 'server_keyfile' ; then
            local keyfile
            keyfile=$(bashio::config 'server_keyfile')
            if [ ! -f "${keyfile}" ]; then
                bashio::log.info "Generating new server key..."
                chisel server --keygen "${keyfile}" || bashio::exit.nok "Failed to generate server key"
                bashio::log.info "Server key generated: ${keyfile}"
            fi
        fi
    fi
}

# ------------------------------------------------------------------------------
# Main execution
# ------------------------------------------------------------------------------
main() {
    bashio::log.info "Initializing Chisel configuration..."
    
    # Check configuration
    checkConfig
    
    # Generate server key if needed
    generateServerKey
    
    bashio::log.info "Chisel configuration completed successfully"
}

# Execute main function
main "$@" 
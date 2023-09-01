import { PageConfig } from '@jupyterlab/coreutils';
import { JupyterProps } from './Jupyter';

/**
 * Type of the Jupyter configuration.
 */
export type IJupyterConfig = {
  jupyterServerHttpUrl: string;
  jupyterServerWsUrl: string;
  jupyterToken: string;
  insideJupyterLab: boolean;
  insideJupyterHub: boolean;
}

/**
 * The default Jupyter configuration.
 */
let config: IJupyterConfig = {
  jupyterServerHttpUrl: '',
  jupyterServerWsUrl: '',
  jupyterToken: '',
  insideJupyterLab: false,
  insideJupyterHub: false,
}

/**
 * Setter for jupyterServerHttpUrl.
 */
export const setJupyterServerHttpUrl = (jupyterServerHttpUrl: string) => {
  config.jupyterServerHttpUrl = jupyterServerHttpUrl;
}
/**
 * Getter for jupyterServerHttpUrl.
 */
 export const getJupyterServerHttpUrl = () => config.jupyterServerHttpUrl;

/**
 * Setter for jupyterServerWsUrl.
 */
 export const setJupyterServerWsUrl = (jupyterServerWsUrl: string) => {
  config.jupyterServerWsUrl = jupyterServerWsUrl;
}
/**
 * Getter for jupyterServerWsUrl.
 */
 export const getJupyterServerWsUrl = () => config.jupyterServerWsUrl;

/**
 * Setter for jupyterToken.
 */
 export const setJupyterToken = (jupyterToken: string) => {
  config.jupyterToken = jupyterToken;
}
/**
 * Getter for jupyterToken.
 */
 export const getJupyterToken = () => config.jupyterToken;

/**
 * Method to load the Jupyter configuration from the
 * host HTML page.
 */
export const loadJupyterConfig = (props: JupyterProps) => {
  const { lite, jupyterServerHttpUrl, jupyterServerWsUrl, collaborative, terminals, jupyterToken } = props;
  const jupyterHtmlConfig = document.getElementById('jupyter-config-data');
  if (jupyterHtmlConfig) {
    const jupyterConfig = JSON.parse(jupyterHtmlConfig.textContent || '');
    setJupyterServerHttpUrl(location.protocol + '//' + location.host + jupyterConfig.baseUrl);
    setJupyterServerWsUrl(location.protocol === "https" ? "wss://" + location.host : "ws://" + location.host + jupyterConfig.baseUrl);
    setJupyterToken(jupyterConfig.token);
    config.insideJupyterLab = jupyterConfig.appName === 'JupyterLab';
  }
  else {
    const datalayerHtmlConfig = document.getElementById('datalayer-config-data');
    if (datalayerHtmlConfig) {
      config = JSON.parse(datalayerHtmlConfig.textContent || '') as IJupyterConfig;
    }
    if (lite) {
      setJupyterServerHttpUrl(location.protocol + '//' + location.host);
    } else if (config.jupyterServerHttpUrl) {
      setJupyterServerHttpUrl(config.jupyterServerHttpUrl);
    } else {
      setJupyterServerHttpUrl(jupyterServerHttpUrl || location.protocol + '//' + location.host + "/api/jupyter");
    }
    if (lite) {
      setJupyterServerWsUrl(location.protocol === "https" ? "wss://" + location.host : "ws://" + location.host);
    } else if (config.jupyterServerWsUrl) {
      setJupyterServerWsUrl(config.jupyterServerWsUrl);
    } else {
      setJupyterServerWsUrl(jupyterServerWsUrl || location.protocol.replace('http', 'ws') + '//' + location.host + "/api/jupyter");
    }
    if (config.jupyterToken) {
      setJupyterToken(config.jupyterToken);
    } else {
      setJupyterToken(jupyterToken || '');
    }  
  }
  PageConfig.setOption('baseUrl', getJupyterServerHttpUrl());
  PageConfig.setOption('wsUrl', getJupyterServerWsUrl());
  PageConfig.setOption('token', getJupyterToken());
  PageConfig.setOption('collaborative', String(collaborative || false));
  PageConfig.setOption('terminalsAvailable', String(terminals || false));
  PageConfig.setOption('mathjaxUrl', 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js');
  PageConfig.setOption('mathjaxConfig', 'TeX-AMS_CHTML-full,Safe');
  /*
  PageConfig.getOption('hubHost')
  PageConfig.getOption('hubPrefix')
  PageConfig.getOption('hubUser')
  PageConfig.getOption('hubServerName')
  */
  config.insideJupyterHub = PageConfig.getOption('hubHost') !== "";
  return config;
}

export const runsInJupyterLab = () => {
  const jupyterHtmlConfig = document.getElementById('jupyter-config-data');
  if (jupyterHtmlConfig) {
    const jupyterConfig = JSON.parse(jupyterHtmlConfig.textContent || '');
    return jupyterConfig.appName === 'JupyterLab';
  }
  return false
}

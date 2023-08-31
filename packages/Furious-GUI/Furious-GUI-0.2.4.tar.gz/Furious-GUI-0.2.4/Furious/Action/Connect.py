from Furious.Core.Core import XrayCore, Hysteria
from Furious.Core.TorRelay import TorRelay
from Furious.Core.Intellisense import Intellisense
from Furious.Core.Configuration import Configuration
from Furious.Action.Routing import BUILTIN_ROUTING_TABLE, BUILTIN_ROUTING
from Furious.Gui.Action import Action
from Furious.Widget.ConnectingProgressBar import ConnectingProgressBar
from Furious.Widget.Widget import MessageBox
from Furious.Utility.Constants import (
    APP,
    APPLICATION_NAME,
    PROXY_SERVER_BYPASS,
    DEFAULT_TOR_HTTPS_PORT,
)
from Furious.Utility.Utility import (
    Switch,
    SupportConnectedCallback,
    bootstrapIcon,
    getAbsolutePath,
)
from Furious.Utility.Translator import gettext as _
from Furious.Utility.Proxy import Proxy

from PySide6 import QtCore
from PySide6.QtTest import QTest
from PySide6.QtNetwork import (
    QNetworkAccessManager,
    QNetworkReply,
    QNetworkRequest,
    QNetworkProxy,
)

import ujson
import random
import logging

logger = logging.getLogger(__name__)


class HttpProxyServerError(Exception):
    pass


class ConnectAction(Action):
    def __init__(self):
        super().__init__(
            _('Connect'),
            icon=bootstrapIcon('unlock-fill.svg'),
            checkable=True,
        )

        self.connectingProgressBar = ConnectingProgressBar()

        self.configurationEmptyBox = MessageBox()
        self.configurationIcingBox = MessageBox()
        self.configurationErrorBox = MessageBox()
        self.configurationTampered = MessageBox()
        self.httpProxyConfErrorBox = MessageBox()

        self.proxyServer = ''

        self.networkAccessManager = QNetworkAccessManager(parent=self)
        self.networkReply = None

        self.coreName = ''
        self.coreText = ''
        self.coreJSON = {}
        self.coreRunning = False
        self.XrayRouting = {}

        self.connectingFlag = False

        self.disconnectReason = ''

        # Note: The connection test is carried out item by item
        # from top to bottom. If any of these succeed,
        # connected action will be executed.

        # "Popular" sites that's been endorsed by some government.
        self.testPool = [
            # Messaging
            'https://telegram.org/',
            # Social media
            'https://twitter.com/',
            # Videos
            'https://www.youtube.com/',
        ]
        self.testTime = 0

        self.XrayCore = XrayCore()
        self.Hysteria = Hysteria()
        self.TorRelay = TorRelay()

    def XrayCoreExitCallback(self, exitcode):
        if self.coreName:
            # If core is running
            assert self.coreRunning
            assert self.coreName == XrayCore.name()

        if exitcode == XrayCore.ExitCode.ConfigurationError:
            if not self.isConnecting():
                # Protect connecting action. Mandatory
                return self.disconnectAction(
                    f'{XrayCore.name()}: {_("Invalid server configuration")}'
                )
            else:
                self.coreRunning = False
                self.disconnectReason = (
                    f'{XrayCore.name()}: {_("Invalid server configuration")}'
                )

                return

        if exitcode == XrayCore.ExitCode.ServerStartFailure:
            if not self.isConnecting():
                # Protect connecting action. Mandatory
                return self.disconnectAction(
                    f'{XrayCore.name()}: {_("Failed to start core")}'
                )
            else:
                self.coreRunning = False
                self.disconnectReason = (
                    f'{XrayCore.name()}: {_("Failed to start core")}'
                )

                return

        if not self.isConnecting():
            # Protect connecting action. Mandatory
            self.disconnectAction(
                f'{XrayCore.name()}: {_("Core terminated unexpectedly")}'
            )
        else:
            self.coreRunning = False
            self.disconnectReason = (
                f'{XrayCore.name()}: {_("Core terminated unexpectedly")}'
            )

    def HysteriaExitCallback(self, exitcode):
        if self.coreName:
            # If core is running
            assert self.coreRunning
            assert self.coreName == Hysteria.name()

        if exitcode == Hysteria.ExitCode.ConfigurationError:
            if not self.isConnecting():
                # Protect connecting action. Mandatory
                return self.disconnectAction(
                    f'{Hysteria.name()}: {_("Invalid server configuration")}'
                )
            else:
                self.coreRunning = False
                self.disconnectReason = (
                    f'{Hysteria.name()}: {_("Invalid server configuration")}'
                )

                return

        if exitcode == Hysteria.ExitCode.RemoteNetworkError:
            if not self.isConnecting():
                # Protect connecting action. Mandatory
                return self.disconnectAction(
                    f'{Hysteria.name()}: {_("Connection to server has been lost")}'
                )
            else:
                self.coreRunning = False
                self.disconnectReason = (
                    f'{Hysteria.name()}: {_("Connection to server has been lost")}'
                )

                return

        if not self.isConnecting():
            # Protect connecting action. Mandatory
            self.disconnectAction(
                f'{Hysteria.name()}: {_("Core terminated unexpectedly")}'
            )
        else:
            self.coreRunning = False
            self.disconnectReason = (
                f'{Hysteria.name()}: {_("Core terminated unexpectedly")}'
            )

    def stopCore(self):
        self.XrayCore.registerExitCallback(None)
        self.Hysteria.registerExitCallback(None)

        # Stop any potentially running core
        self.XrayCore.stop()
        self.Hysteria.stop()

        self.TorRelay.stop()

        self.coreRunning = False

    def showConnectingProgressBar(self):
        if APP().ShowProgressBarWhenConnecting == Switch.ON_:
            self.connectingProgressBar.progressBar.setValue(0)
            # Update the progress bar every 50ms
            self.connectingProgressBar.timer.start(50)
            self.connectingProgressBar.show()

        return self

    def hideConnectingProgressBar(self, done=False):
        if done:
            self.connectingProgressBar.progressBar.setValue(100)

        self.connectingProgressBar.hide()
        self.connectingProgressBar.timer.stop()

        return self

    def moveConnectingProgressBar(self):
        # Progressing
        if self.connectingProgressBar.progressBar.value() <= 45:
            self.connectingProgressBar.progressBar.setValue(random.randint(45, 50))
        # Lower timer frequency
        self.connectingProgressBar.timer.start(250)

        return self

    def setDisabledAction(self, value):
        self.setDisabled(value)

        APP().tray.RoutingAction.setDisabled(value)

    def setConnectingStatus(self, showProgressBar=True):
        if showProgressBar:
            self.showConnectingProgressBar()

        # Do not accept new action
        self.setDisabledAction(True)
        self.setText(_('Connecting'))
        self.setIcon(bootstrapIcon('lock-fill.svg'))

    def setConnectedStatus(self):
        self.hideConnectingProgressBar(done=True)
        self.setDisabledAction(False)

        APP().tray.setConnectedIcon()

        # Finished. Reset connecting flag
        self.connectingFlag = False

        # Connected
        self.setText(_('Disconnect'))

        SupportConnectedCallback.callConnectedCallback()

    def isConnecting(self):
        return self.connectingFlag

    def isConnected(self):
        return self.textCompare('Disconnect')

    def reset(self):
        # Reset everything

        self.stopCore()

        self.hideConnectingProgressBar()
        self.setText(_('Connect'))
        self.setIcon(bootstrapIcon('unlock-fill.svg'))
        self.setChecked(False)

        APP().Connect = Switch.OFF
        APP().tray.setPlainIcon()

        self.proxyServer = ''

        self.coreName = ''
        self.coreText = ''
        self.coreJSON = {}
        self.coreRunning = False
        self.XrayRouting = {}

        # Accept new action
        self.setDisabledAction(False)

        self.disconnectReason = ''

        self.connectingFlag = False

    @property
    def activatedServer(self):
        try:
            activatedIndex = int(APP().ActivatedItemIndex)

            if activatedIndex < 0:
                return None
            else:
                return APP().ServerWidget.ServerList[activatedIndex]['config']

        except Exception:
            # Any non-exit exceptions

            return None

    def errorConfiguration(self):
        self.configurationErrorBox.setIcon(MessageBox.Icon.Critical)
        self.configurationErrorBox.setWindowTitle(_('Unable to connect'))
        self.configurationErrorBox.setText(_('Invalid server configuration.'))

        # Show the MessageBox and wait for user to close it
        self.configurationErrorBox.exec()

    def errorConfigurationEmpty(self):
        self.configurationEmptyBox.setIcon(MessageBox.Icon.Critical)
        self.configurationEmptyBox.setWindowTitle(_('Unable to connect'))
        self.configurationEmptyBox.setText(
            _('Server configuration empty. Please configure your server first.')
        )

        # Show the MessageBox and wait for user to close it
        self.configurationEmptyBox.exec()

    def errorConfigurationNotActivated(self):
        self.configurationIcingBox.setIcon(MessageBox.Icon.Information)
        self.configurationIcingBox.setWindowTitle(_('Unable to connect'))
        self.configurationIcingBox.setText(
            _('Select and double click to activate configuration and connect.')
        )

        # Show the MessageBox and wait for user to close it
        self.configurationIcingBox.exec()

    def errorHttpProxyConf(self):
        self.httpProxyConfErrorBox.setIcon(MessageBox.Icon.Critical)
        self.httpProxyConfErrorBox.setWindowTitle(_('Unable to connect'))
        self.httpProxyConfErrorBox.setText(
            _(
                f'{APPLICATION_NAME} cannot find any valid http proxy '
                f'endpoint in your server configuration.'
            )
        )
        self.httpProxyConfErrorBox.setInformativeText(
            _('Please complete your server configuration.')
        )

        # Show the MessageBox and wait for user to close it
        self.httpProxyConfErrorBox.exec()

    @property
    def torRelayStorageObj(self):
        # Handy reference
        return APP().torRelaySettingsWidget.StorageObj

    def configureCore(self):
        def validateProxyServer(server):
            # Validate proxy server
            try:
                host, port = server.split(':')

                if int(port) < 0 or int(port) > 65535:
                    raise ValueError
            except Exception:
                # Any non-exit exceptions

                self.reset()
                self.errorHttpProxyConf()

                return False
            else:
                self.proxyServer = server

                return True

        self.stopCore()

        self.XrayCore.registerExitCallback(
            lambda exitcode: self.XrayCoreExitCallback(exitcode)
        )
        self.Hysteria.registerExitCallback(
            lambda exitcode: self.HysteriaExitCallback(exitcode)
        )

        proxyServer = None

        if Intellisense.getCoreType(self.coreJSON) == XrayCore.name():
            # Assuming is XrayCore configuration
            proxyHost = None
            proxyPort = None

            try:
                for inbound in self.coreJSON['inbounds']:
                    if inbound['protocol'] == 'http':
                        proxyHost = inbound['listen']
                        proxyPort = inbound['port']

                        # Note: If there are multiple http inbounds
                        # satisfied, the first one will be chosen.
                        break

                if proxyHost is None or proxyPort is None:
                    # No HTTP proxy endpoint configured
                    raise HttpProxyServerError

                proxyServer = f'{proxyHost}:{proxyPort}'
            except (KeyError, HttpProxyServerError):
                self.reset()
                self.errorHttpProxyConf()
            else:
                if validateProxyServer(proxyServer):
                    routing = APP().Routing

                    logger.info(f'core {XrayCore.name()} configured')

                    def fixLoggingRelativePath(attr):
                        # Relative path fails if booting on start up
                        # on Windows, when packed using nuitka...

                        # Fix relative path if needed. User cannot feel this operation.

                        try:
                            path = self.coreJSON['log'][attr]
                        except KeyError:
                            pass
                        else:
                            if path and (
                                isinstance(path, str) or isinstance(path, bytes)
                            ):
                                fix = getAbsolutePath(path)

                                logger.info(
                                    f'{XrayCore.name()}: {attr} log is specified as \'{path}\'. '
                                    f'Fixed to \'{fix}\''
                                )

                                self.coreJSON['log'][attr] = fix

                    fixLoggingRelativePath('access')
                    fixLoggingRelativePath('error')

                    # Filter Route My Traffic Through Tor, Custom
                    if routing in list(
                        filter(
                            lambda x: x != 'Route My Traffic Through Tor'
                            and x != 'Custom',
                            BUILTIN_ROUTING,
                        )
                    ):
                        routingObject = BUILTIN_ROUTING_TABLE[routing][XrayCore.name()]

                        logger.info(f'routing is {routing}')
                        logger.info(f'RoutingObject: {routingObject}')

                        self.coreJSON['routing'] = routingObject
                    elif routing == 'Route My Traffic Through Tor':
                        logger.info(f'routing is {routing}')

                        if TorRelay.checkIfExists():
                            logger.info(
                                f'find Tor CLI in path success. Version: {TorRelay.version()}'
                            )

                            routingObject = {}

                            logger.info(f'RoutingObject: {routingObject}')

                            self.coreJSON['routing'] = routingObject
                        else:
                            logger.error('find Tor CLI in path failed')

                            self.coreRunning = False

                            self.disconnectReason = (
                                f'{XrayCore.name()}: {_("Cannot find Tor CLI in PATH")}'
                            )

                            return XrayCore.name()
                    elif routing == 'Custom':
                        logger.info(f'routing is {routing}')
                        logger.info(f'RoutingObject: {self.XrayRouting}')

                        # Assign user routing
                        self.coreJSON['routing'] = self.XrayRouting
                    else:
                        try:
                            routesWidget = APP().RoutesWidget

                            route = routesWidget.RoutesList[int(routing)]

                            logger.info(f'routing is {route["remark"]}')
                            logger.info(f'RoutingObject: {route[XrayCore.name()]}')

                            self.coreJSON['routing'] = route[XrayCore.name()]
                        except Exception as ex:
                            # Any non-exit exceptions

                            logger.error(
                                f'get custom routing object failed: {ex}. Fast fail'
                            )

                            # Fast fail
                            self.coreJSON = {}

                    self.coreRunning = True

                    # Refresh configuration modified before. User cannot feel
                    self.coreText = ujson.dumps(
                        self.coreJSON, ensure_ascii=False, escape_forward_slashes=False
                    )
                    # Start core
                    self.XrayCore.start(self.coreText)

                    if routing == 'Route My Traffic Through Tor':
                        self.startTorRelay(XrayCore.name(), proxyServer)

            return XrayCore.name()

        if Intellisense.getCoreType(self.coreJSON) == Hysteria.name():
            # Assuming is Hysteria configuration
            try:
                proxyServer = self.coreJSON['http']['listen']

                if proxyServer is None:
                    # No HTTP proxy endpoint configured
                    raise HttpProxyServerError
            except (KeyError, HttpProxyServerError):
                self.reset()
                self.errorHttpProxyConf()
            else:
                if validateProxyServer(proxyServer):
                    self.coreRunning = True

                    routing = APP().Routing

                    logger.info(f'core {Hysteria.name()} configured')

                    # Filter Route My Traffic Through Tor, Global, Custom
                    if routing in list(
                        filter(
                            lambda x: x != 'Route My Traffic Through Tor'
                            and x != 'Global'
                            and x != 'Custom',
                            BUILTIN_ROUTING,
                        )
                    ):
                        logger.info(f'routing is {routing}')

                        routingObject = BUILTIN_ROUTING_TABLE[routing][Hysteria.name()]

                        self.Hysteria.start(
                            self.coreText,
                            Hysteria.rule(routingObject.get('acl')),
                            Hysteria.mmdb(routingObject.get('mmdb')),
                        )
                    elif routing == 'Route My Traffic Through Tor':
                        logger.info(f'routing is {routing}')

                        if TorRelay.checkIfExists():
                            logger.info(
                                f'find Tor CLI in path success. Version: {TorRelay.version()}'
                            )

                            self.Hysteria.start(self.coreText, '', '')

                            self.startTorRelay(Hysteria.name(), proxyServer)
                        else:
                            logger.error('find Tor CLI in path failed')

                            self.coreRunning = False

                            self.disconnectReason = (
                                f'{Hysteria.name()}: {_("Cannot find Tor CLI in PATH")}'
                            )

                            return Hysteria.name()
                    elif routing == 'Global':
                        logger.info(f'routing is {routing}')

                        self.Hysteria.start(self.coreText, '', '')
                    elif routing == 'Custom':
                        logger.info(f'routing is {routing}')

                        self.Hysteria.start(
                            self.coreText,
                            Hysteria.rule(self.coreJSON.get('acl')),
                            Hysteria.mmdb(self.coreJSON.get('mmdb')),
                        )
                    else:
                        try:
                            routesWidget = APP().RoutesWidget

                            route = routesWidget.RoutesList[int(routing)]

                            logger.info(f'routing is {route["remark"]}')
                            logger.info(f'RoutingObject: {route[Hysteria.name()]}')

                            self.Hysteria.start(
                                self.coreText,
                                Hysteria.rule(route[Hysteria.name()].get('acl')),
                                Hysteria.mmdb(route[Hysteria.name()].get('mmdb')),
                            )
                        except Exception as ex:
                            # Any non-exit exceptions

                            logger.error(
                                f'get custom routing object failed: {ex}. Fast fail'
                            )

                            # Fast fail
                            self.Hysteria.start('', '', '')

            return Hysteria.name()

        # No matching core
        return ''

    def startTorRelay(self, core, proxyServer, startCounter=0, step=1):
        # Redirect Proxy
        self.proxyServer = f'127.0.0.1:{self.torRelayStorageObj.get("httpsTunnelPort", DEFAULT_TOR_HTTPS_PORT)}'

        try:
            timeout = 1000 * int(
                self.torRelayStorageObj.get('relayEstablishTimeout', 15)
            )
        except Exception:
            # Any non-exit exceptions

            # 15s
            timeout = 1000 * 15

        logger.info(f'{TorRelay.name()} bootstrap timeout is {timeout // 1000}s')

        # Start Tor Relay
        if self.torRelayStorageObj.get('useProxy', True):
            # Use proxy
            self.TorRelay.start(proxyServer=proxyServer)
        else:
            # Do not use proxy
            self.TorRelay.start()

        while (
            self.coreRunning
            and startCounter < timeout
            and self.TorRelay.bootstrapPercentage != 100
        ):
            QTest.qWait(step)

            startCounter += step

        if not self.coreRunning:
            # Interrupted externally. Return
            return

        if self.TorRelay.bootstrapPercentage != 100:
            # bootstrap timeout
            self.stopCore()
            # Assign disconnect reason
            self.disconnectReason = (
                f'{core}: {_(f"{TorRelay.name()} establish timeout")}'
            )

            logger.error(f'{TorRelay.name()} establish failed')
        else:
            logger.info(f'{TorRelay.name()} establish success')

    def startConnectionTest(
        self, showRoutingChangedMessage=False, currentRouting='', isBuiltinRouting=False
    ):
        selected = self.testPool[self.testTime]

        self.testTime += 1

        logger.info(f'start connection test. Try: {selected}')

        # Checked. split should not throw exceptions
        proxyHost, proxyPort = self.proxyServer.split(':')

        # Checked. int(proxyPort) should not throw exceptions
        self.networkAccessManager.setProxy(
            QNetworkProxy(QNetworkProxy.ProxyType.HttpProxy, proxyHost, int(proxyPort))
        )

        self.networkReply = self.networkAccessManager.get(
            QNetworkRequest(QtCore.QUrl(selected))
        )

        @QtCore.Slot()
        def finishedCallback():
            assert isinstance(self.networkReply, QNetworkReply)

            if self.networkReply.error() != QNetworkReply.NetworkError.NoError:
                logger.error(
                    f'{self.coreName}: connection test failed. {self.networkReply.errorString()}'
                )

                if self.testTime < len(self.testPool) and self.coreRunning:
                    # Try next
                    self.startConnectionTest(
                        showRoutingChangedMessage, currentRouting, isBuiltinRouting
                    )
                else:
                    if self.disconnectReason:
                        self.disconnectAction(self.disconnectReason)
                    else:
                        self.disconnectAction(
                            f'{self.coreName}: {_("Connection test failed")}'
                        )
            else:
                logger.info(f'{self.coreName}: connection test success. Connected')

                APP().Connect = Switch.ON_

                # Connected status
                self.setConnectedStatus()

                if showRoutingChangedMessage:
                    # Routing changed
                    if isBuiltinRouting:
                        APP().tray.showMessage(
                            _('Routing changed: ') + _(currentRouting)
                        )
                    else:
                        APP().tray.showMessage(_('Routing changed: ') + currentRouting)
                else:
                    # Connected
                    APP().tray.showMessage(f'{self.coreName}: {_("Connected")}')

        self.networkReply.finished.connect(finishedCallback)

    def connectAction(self):
        # Connect action
        assert self.textCompare('Connect')

        # Connecting
        self.connectingFlag = True

        if not APP().Configuration or len(APP().ServerWidget.ServerList) == 0:
            APP().Connect = Switch.OFF

            self.setChecked(False)
            self.connectingFlag = False
            self.errorConfigurationEmpty()

            return

        myText = self.activatedServer

        if myText is None:
            APP().Connect = Switch.OFF

            self.setChecked(False)
            self.connectingFlag = False
            self.errorConfigurationNotActivated()

            return

        if myText == '':
            APP().Connect = Switch.OFF

            self.setChecked(False)
            self.connectingFlag = False
            self.errorConfigurationEmpty()

            return

        try:
            myJSON = Configuration.toJSON(myText)
        except Exception:
            # Any non-exit exceptions

            APP().Connect = Switch.OFF

            self.setChecked(False)
            self.connectingFlag = False

            # Invalid configuratoin
            self.errorConfiguration()
        else:
            # Get server configuration success. Continue.
            # Note: use self.reset() to restore state

            self.coreText = myText
            self.coreJSON = myJSON

            # Memorize user routing if possible
            self.XrayRouting = myJSON.get('routing', {})

            self.connectingAction()

    def connectingAction(
        self,
        showProgressBar=True,
        showRoutingChangedMessage=False,
        currentRouting='',
        isBuiltinRouting=False,
        **kwargs,
    ):
        # Connecting. Redefined
        self.connectingFlag = True

        # Connecting status
        self.setConnectingStatus(showProgressBar)

        # Configure connect
        self.coreName = self.configureCore()

        if not self.coreName:
            # No matching core
            self.reset()
            self.errorConfiguration()

            return

        if not self.coreRunning:
            # 1. No valid HTTP proxy endpoint. reset / disconnect has been called

            if self.isConnecting():
                # 2. Core has exited

                self.disconnectAction(self.disconnectReason)

            return

        try:
            Proxy.set(self.proxyServer, PROXY_SERVER_BYPASS)
        except Exception:
            # Any non-exit exceptions

            Proxy.off()

            self.reset()
            self.errorConfiguration()
        else:
            self.moveConnectingProgressBar()
            # Reset try time
            self.testTime = 0
            self.startConnectionTest(
                showRoutingChangedMessage, currentRouting, isBuiltinRouting
            )

    def disconnectAction(self, reason=''):
        Proxy.off()

        self.reset()

        SupportConnectedCallback.callDisconnectedCallback()

        APP().tray.showMessage(reason)

    def reconnectAction(self, reason=''):
        self.disconnectAction(reason)
        self.trigger()

    def triggeredCallback(self, checked):
        if checked:
            self.connectAction()
        else:
            # Disconnect action
            assert self.textCompare('Disconnect')
            assert self.connectingFlag is False

            self.disconnectAction(f'{self.coreName}: {_("Disconnected")}')

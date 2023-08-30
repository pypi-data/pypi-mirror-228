import pytest

import bellows.ezsp.v12

from .async_mock import AsyncMock, MagicMock, patch


@pytest.fixture
def ezsp_f():
    """EZSP v12 protocol handler."""
    return bellows.ezsp.v12.EZSPv12(MagicMock(), MagicMock())


def test_ezsp_frame(ezsp_f):
    ezsp_f._seq = 0x22
    data = ezsp_f._ezsp_frame("version", 12)
    assert data == b"\x22\x00\x01\x00\x00\x0c"


def test_ezsp_frame_rx(ezsp_f):
    """Test receiving a version frame."""
    ezsp_f(b"\x01\x01\x80\x00\x00\x01\x02\x34\x12")
    assert ezsp_f._handle_callback.call_count == 1
    assert ezsp_f._handle_callback.call_args[0][0] == "version"
    assert ezsp_f._handle_callback.call_args[0][1] == [0x01, 0x02, 0x1234]


async def test_pre_permit(ezsp_f):
    """Test pre permit."""
    p1 = patch.object(ezsp_f, "setPolicy", new=AsyncMock())
    p2 = patch.object(ezsp_f, "addTransientLinkKey", new=AsyncMock())
    with p1 as pre_permit_mock, p2 as tclk_mock:
        await ezsp_f.pre_permit(-1.9)
    assert pre_permit_mock.await_count == 2
    assert tclk_mock.await_count == 1


def test_command_frames(ezsp_f):
    """Test alphabetical list of frames matches the commands."""
    assert set(ezsp_f.COMMANDS) == set(command_frames)
    for name, frame_id in command_frames.items():
        assert ezsp_f.COMMANDS[name][0] == frame_id
        assert ezsp_f.COMMANDS_BY_ID[frame_id][0] == name


command_frames = {
    "addEndpoint": 0x0002,
    "addOrUpdateKeyTableEntry": 0x0066,
    "addressTableEntryIsActive": 0x005B,
    "addTransientLinkKey": 0x00AF,
    "aesEncrypt": 0x0094,
    "aesMmoHash": 0x006F,
    "becomeTrustCenter": 0x0077,
    "bindingIsActive": 0x002E,
    "bootloadTransmitCompleteHandler": 0x0093,
    "broadcastNetworkKeySwitch": 0x0074,
    "broadcastNextNetworkKey": 0x0073,
    "calculateSmacs": 0x009F,
    "calculateSmacs283k1": 0x00EA,
    "calculateSmacsHandler": 0x00A0,
    "calculateSmacsHandler283k1": 0x00EB,
    "callback": 0x0006,
    "checkKeyContext": 0x0110,
    "childId": 0x0106,
    "childJoinHandler": 0x0023,
    "clearBindingTable": 0x002A,
    "clearKeyTable": 0x00B1,
    "clearStoredBeacons": 0x003C,
    "clearTemporaryDataMaybeStoreLinkKey": 0x00A1,
    "clearTemporaryDataMaybeStoreLinkKey283k1": 0x00EE,
    "clearTransientLinkKeys": 0x006B,
    "counterRolloverHandler": 0x00F2,
    "customFrame": 0x0047,
    "customFrameHandler": 0x0054,
    "debugWrite": 0x0012,
    "delayTest": 0x009D,
    "deleteBinding": 0x002D,
    "dGpSend": 0x00C6,
    "dGpSentHandler": 0x00C7,
    "dsaSign": 0x00A6,
    "dsaSignHandler": 0x00A7,
    "dsaVerify": 0x00A3,
    "dsaVerify283k1": 0x00B0,
    "dsaVerifyHandler": 0x0078,
    "dutyCycleHandler": 0x004D,
    "echo": 0x0081,
    "energyScanRequest": 0x009C,
    "energyScanResultHandler": 0x0048,
    "eraseKeyTableEntry": 0x0076,
    "exportKey": 0x0114,
    "exportLinkKeyByEui": 0x010D,
    "exportLinkKeyByIndex": 0x010F,
    "exportTransientKeyByEui": 0x0113,
    "exportTransientKeyByIndex": 0x0112,
    "findAndRejoinNetwork": 0x0021,
    "findKeyTableEntry": 0x0075,
    "findUnusedPanId": 0x00D3,
    "formNetwork": 0x001E,
    "generateCbkeKeys": 0x00A4,
    "generateCbkeKeys283k1": 0x00E8,
    "generateCbkeKeysHandler": 0x009E,
    "generateCbkeKeysHandler283k1": 0x00E9,
    "getAddressTableRemoteEui64": 0x005E,
    "getAddressTableRemoteNodeId": 0x005F,
    "getApsKeyInfo": 0x010C,
    "getBeaconClassificationParams": 0x00F3,
    "getBinding": 0x002C,
    "getBindingRemoteNodeId": 0x002F,
    "getCertificate": 0x00A5,
    "getCertificate283k1": 0x00EC,
    "getChildData": 0x004A,
    "getConfigurationValue": 0x0052,
    "getCurrentDutyCycle": 0x004C,
    "getCurrentSecurityState": 0x0069,
    "getDutyCycleLimits": 0x004B,
    "getDutyCycleState": 0x0035,
    "getEui64": 0x0026,
    "getExtendedTimeout": 0x007F,
    "getExtendedValue": 0x0003,
    "getFirstBeacon": 0x003D,
    "getKey": 0x006A,
    "getKeyTableEntry": 0x0071,
    "getLibraryStatus": 0x0001,
    "getLogicalChannel": 0x00BA,
    "getMfgToken": 0x000B,
    "getMulticastTableEntry": 0x0063,
    "getNeighbor": 0x0079,
    "getNeighborFrameCounter": 0x003E,
    "getNetworkParameters": 0x0028,
    "getNextBeacon": 0x0004,
    "getNodeId": 0x0027,
    "getNumStoredBeacons": 0x0008,
    "getParentChildParameters": 0x0029,
    "getParentClassificationEnabled": 0x00F0,
    "getPhyInterfaceCount": 0x00FC,
    "getPolicy": 0x0056,
    "getRadioParameters": 0x00FD,
    "getRandomNumber": 0x0049,
    "getRouteTableEntry": 0x007B,
    "getRoutingShortcutThreshold": 0x00D1,
    "getSecurityKeyStatus": 0x00CD,
    "getSourceRouteTableEntry": 0x00C1,
    "getSourceRouteTableFilledSize": 0x00C2,
    "getSourceRouteTableTotalSize": 0x00C3,
    "getStandaloneBootloaderVersionPlatMicroPhy": 0x0091,
    "getTimer": 0x004E,
    "getToken": 0x000A,
    "getTokenCount": 0x0100,
    "getTokenData": 0x0102,
    "getTokenInfo": 0x0101,
    "getTransientKeyTableEntry": 0x006D,
    "getTransientLinkKey": 0x00CE,
    "getTrueRandomEntropySource": 0x004F,
    "getValue": 0x00AA,
    "getXncpInfo": 0x0013,
    "getZllPrimaryChannelMask": 0x00D9,
    "getZllSecondaryChannelMask": 0x00DA,
    "gpepIncomingMessageHandler": 0x00C5,
    "gpProxyTableGetEntry": 0x00C8,
    "gpProxyTableLookup": 0x00C0,
    "gpProxyTableProcessGpPairing": 0x00C9,
    "gpSinkCommission": 0x010A,
    "gpSinkTableClearAll": 0x00E2,
    "gpSinkTableFindOrAllocateEntry": 0x00E1,
    "gpSinkTableGetEntry": 0x00DD,
    "gpSinkTableInit": 0x0070,
    "gpSinkTableLookup": 0x00DE,
    "gpSinkTableRemoveEntry": 0x00E0,
    "gpSinkTableSetEntry": 0x00DF,
    "gpTranslationTableClear": 0x010B,
    "idConflictHandler": 0x007C,
    "importKey": 0x0115,
    "importLinkKey": 0x010E,
    "importTransientKey": 0x0111,
    "incomingBootloadMessageHandler": 0x0092,
    "incomingManyToOneRouteRequestHandler": 0x007D,
    "incomingMessageHandler": 0x0045,
    "incomingNetworkStatusHandler": 0x00C4,
    "incomingRouteErrorHandler": 0x0080,
    "incomingRouteRecordHandler": 0x0059,
    "incomingSenderEui64Handler": 0x0062,
    "invalidCommand": 0x0058,
    "isHubConnected": 0x00E6,
    "isUpTimeLong": 0x00E5,
    "isZllNetwork": 0x00BE,
    "joinNetwork": 0x001F,
    "joinNetworkDirectly": 0x003B,
    "launchStandaloneBootloader": 0x008F,
    "leaveNetwork": 0x0020,
    "lookupEui64ByNodeId": 0x0061,
    "lookupNodeIdByEui64": 0x0060,
    "macFilterMatchMessageHandler": 0x0046,
    "macPassthroughMessageHandler": 0x0097,
    "maximumPayloadLength": 0x0033,
    "messageSentHandler": 0x003F,
    "mfglibEnd": 0x0084,
    "mfglibGetChannel": 0x008B,
    "mfglibGetPower": 0x008D,
    "mfglibRxHandler": 0x008E,
    "mfglibSendPacket": 0x0089,
    "mfglibSetChannel": 0x008A,
    "mfglibSetPower": 0x008C,
    "mfglibStart": 0x0083,
    "mfglibStartStream": 0x0087,
    "mfglibStartTone": 0x0085,
    "mfglibStopStream": 0x0088,
    "mfglibStopTone": 0x0086,
    "multiPhySetRadioChannel": 0x00FB,
    "multiPhySetRadioPower": 0x00FA,
    "multiPhyStart": 0x00F8,
    "multiPhyStop": 0x00F9,
    "neighborCount": 0x007A,
    "networkFoundHandler": 0x001B,
    "networkInit": 0x0017,
    "networkState": 0x0018,
    "noCallbacks": 0x0007,
    "nop": 0x0005,
    "permitJoining": 0x0022,
    "pollCompleteHandler": 0x0043,
    "pollForData": 0x0042,
    "pollHandler": 0x0044,
    "proxyBroadcast": 0x0037,
    "rawTransmitCompleteHandler": 0x0098,
    "readAndClearCounters": 0x0065,
    "readAttribute": 0x0108,
    "readCounters": 0x00F1,
    "remoteDeleteBindingHandler": 0x0032,
    "remoteSetBindingHandler": 0x0031,
    "removeDevice": 0x00A8,
    "replaceAddressTableEntry": 0x0082,
    "requestLinkKey": 0x0014,
    "resetNode": 0x0104,
    "resetToFactoryDefaults": 0x00CC,
    "scanCompleteHandler": 0x001C,
    "sendBootloadMessage": 0x0090,
    "sendBroadcast": 0x0036,
    "sendLinkPowerDeltaRequest": 0x00F7,
    "sendManyToOneRouteRequest": 0x0041,
    "sendMulticast": 0x0038,
    "sendMulticastWithAlias": 0x003A,
    "sendPanIdUpdate": 0x0057,
    "sendRawMessage": 0x0096,
    "sendRawMessageExtended": 0x0051,
    "sendReply": 0x0039,
    "sendTrustCenterLinkKey": 0x0067,
    "sendUnicast": 0x0034,
    "setAddressTableRemoteEui64": 0x005C,
    "setAddressTableRemoteNodeId": 0x005D,
    "setBeaconClassificationParams": 0x00EF,
    "setBinding": 0x002B,
    "setBindingRemoteNodeId": 0x0030,
    "setBrokenRouteErrorCode": 0x0011,
    "setChildData": 0x00AC,
    "setChildData": 0x00AC,
    "setConcentrator": 0x0010,
    "setConfigurationValue": 0x0053,
    "setDutyCycleLimitsInStack": 0x0040,
    "setExtendedTimeout": 0x007E,
    "setHubConnectivity": 0x00E4,
    "setInitialSecurityState": 0x0068,
    "setKeyTableEntry": 0x0072,
    "setLogicalAndRadioChannel": 0x00B9,
    "setLongUpTime": 0x00E3,
    "setMacPollFailureWaitTime": 0x00F4,
    "setManufacturerCode": 0x0015,
    "setMfgToken": 0x000C,
    "setMulticastTableEntry": 0x0064,
    "setNeighborFrameCounter": 0x00AD,
    "setNeighborFrameCounter": 0x00AD,
    "setParentClassificationEnabled": 0x00E7,
    "setPassiveAckConfig": 0x0105,
    "setPolicy": 0x0055,
    "setPowerDescriptor": 0x0016,
    "setPreinstalledCbkeData": 0x00A2,
    "setPreinstalledCbkeData283k1": 0x00ED,
    "setRadioChannel": 0x009A,
    "setRadioIeee802154CcaMode": 0x0095,
    "setRadioIeee802154CcaMode": 0x0095,
    "setRadioPower": 0x0099,
    "setRoutingShortcutThreshold": 0x00D0,
    "setSecurityKey": 0x00CA,
    "setSecurityParameters": 0x00CB,
    "setSourceRouteDiscoveryMode": 0x005A,
    "setTimer": 0x000E,
    "setToken": 0x0009,
    "setTokenData": 0x0103,
    "setValue": 0x00AB,
    "setZllAdditionalState": 0x00D6,
    "setZllNodeType": 0x00D5,
    "setZllPrimaryChannelMask": 0x00DB,
    "setZllSecondaryChannelMask": 0x00DC,
    "stackStatusHandler": 0x0019,
    "stackTokenChangedHandler": 0x000D,
    "startScan": 0x001A,
    "stopScan": 0x001D,
    "switchNetworkKeyHandler": 0x006E,
    "timerHandler": 0x000F,
    "trustCenterJoinHandler": 0x0024,
    "unicastCurrentNetworkKey": 0x0050,
    "unicastNwkKeyUpdate": 0x00A9,
    "unusedPanIdFoundHandler": 0x00D2,
    "updateTcLinkKey": 0x006C,
    "version": 0x0000,
    "writeAttribute": 0x0109,
    "writeNodeData": 0x00FE,
    "zigbeeKeyEstablishmentHandler": 0x009B,
    "zllAddressAssignmentHandler": 0x00B8,
    "zllClearTokens": 0x0025,
    "zllGetTokens": 0x00BC,
    "zllNetworkFoundHandler": 0x00B6,
    "zllNetworkOps": 0x00B2,
    "zllOperationInProgress": 0x00D7,
    "zllRxOnWhenIdleGetActive": 0x00D8,
    "zllScanCompleteHandler": 0x00B7,
    "zllSetDataToken": 0x00BD,
    "zllSetInitialSecurityState": 0x00B3,
    "zllSetNonZllNetwork": 0x00BF,
    "zllSetRadioIdleMode": 0x00D4,
    "zllSetRxOnWhenIdle": 0x00B5,
    "zllSetSecurityStateWithoutKey": 0x00CF,
    "zllStartScan": 0x00B4,
    "zllTouchLinkTargetHandler": 0x00BB,
}

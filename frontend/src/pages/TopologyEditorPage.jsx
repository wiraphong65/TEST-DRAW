// frontend/src/pages/TopologyEditorPage.jsx
import React, { useState, useRef, useEffect } from 'react';
import { Stage, Layer, Line } from 'react-konva';
import DeviceNode from '../components/topology/DeviceNode';
import PropertyEditor from '../components/topology/PropertyEditor'; // New import

const TopologyEditorPage = () => {
  const [devices, setDevices] = useState([
    {
      id: `client-${Date.now()}-1`,
      name: 'Router0',
      x: 50, y: 50,
      type: 'Router',
      properties: { num_ports: 4, total_bandwidth: 1000, throughput_per_port: 250, estimated_load: 100 }
    },
    {
      id: `client-${Date.now()}-2`,
      name: 'Switch0',
      x: 200, y: 150,
      type: 'Switch',
      properties: { num_ports: 8, total_bandwidth: 1000, throughput_per_port: 100, estimated_load: 50 }
    },
  ]);
  const [linkingSourceDeviceId, setLinkingSourceDeviceId] = useState(null); // For drawing links
  const [editingDevice, setEditingDevice] = useState(null); // For property editor
  const [links, setLinks] = useState([]);
  const stageRef = useRef(null);

  const handleAddDevice = () => {
    const newId = `client-${Date.now()}-${devices.length + 1}`;
    const deviceNum = devices.length;
    setDevices([
      ...devices,
      {
        id: newId,
        name: `Device-${deviceNum}`,
        x: 100, y: 100,
        type: 'PC',
        properties: { num_ports: 1, total_bandwidth: 100, throughput_per_port: 100, estimated_load: 10 }
      },
    ]);
  };

  const handleDeviceDragEnd = (id, e) => {
    const newDevices = devices.map((device) =>
      device.id === id ? { ...device, x: e.target.x(), y: e.target.y() } : device
    );
    setDevices(newDevices);

    if (editingDevice && editingDevice.id === id) {
        // Find the updated device from newDevices array to ensure properties are also current
        const updatedDeviceInstance = newDevices.find(d => d.id === id);
        setEditingDevice(updatedDeviceInstance);
    }
  };

  const handleDeviceClick = (clickedDeviceId) => {
    const device = devices.find(d => d.id === clickedDeviceId);
    if (!device) return;

    if (linkingSourceDeviceId) {
      if (linkingSourceDeviceId !== clickedDeviceId) {
        setLinks(prevLinks => [...prevLinks, {id: `link-${Date.now()}`, sourceId: linkingSourceDeviceId, targetId: clickedDeviceId}]);
        setLinkingSourceDeviceId(null);
        setEditingDevice(null);
      } else {
        setLinkingSourceDeviceId(null);
        setEditingDevice(device);
      }
    } else {
      setEditingDevice(device);
      setLinkingSourceDeviceId(clickedDeviceId);
    }
  };

  const handleUpdateDeviceProperties = (deviceId, updatedProps) => {
    let changedDeviceInstance = null;
    setDevices(prevDevices => prevDevices.map(device => {
      if (device.id === deviceId) {
        changedDeviceInstance = {
          ...device,
          name: updatedProps.name,
          type: updatedProps.device_type, // Note: 'type' on device, 'device_type' in form
          properties: {
            // ...device.properties, // Keep existing unspecified properties from device.properties
            num_ports: updatedProps.num_ports,
            total_bandwidth: updatedProps.total_bandwidth,
            throughput_per_port: updatedProps.throughput_per_port,
            estimated_load: updatedProps.estimated_load,
          }
        };
        return changedDeviceInstance;
      }
      return device;
    }));

    // Update editingDevice as well to reflect changes immediately in the form
    if (editingDevice && editingDevice.id === deviceId && changedDeviceInstance) {
        setEditingDevice(changedDeviceInstance);
    }
  };

  const handleDeselectDevice = () => {
    setEditingDevice(null);
    setLinkingSourceDeviceId(null);
  };

  const getDeviceCenter = (deviceId) => {
    const device = devices.find(d => d.id === deviceId);
    if (!device) return { x: 0, y: 0 };
    return { x: device.x + 50, y: device.y + 25 };
  };

  const handleStageClick = (e) => {
    if (e.target === stageRef.current) { // Check if the click is on the stage itself
      handleDeselectDevice();
    }
  };

  return (
    <div style={{ display: 'flex', fontFamily: 'Arial, sans-serif' }}>
      <div style={{flexGrow: 1}}>
        <h2>Topology Editor</h2>
        <div style={{marginBottom: '10px'}}>
            <button onClick={handleAddDevice}>Add Device</button>
        </div>

        {linkingSourceDeviceId && !editingDevice &&
            <p style={{color: 'blue'}}>Linking from: {devices.find(d=>d.id === linkingSourceDeviceId)?.name}. Click another device to link.</p>}
        {editingDevice &&
            <p style={{color: 'green'}}>
                Selected for Editing: {editingDevice.name}.
                {linkingSourceDeviceId === editingDevice.id ? " Click another device to link or deselect." : ""}
            </p>}


        <Stage
          width={window.innerWidth * 0.65} // Adjusted width
          height={window.innerHeight * 0.7}
          style={{ border: '1px solid grey', backgroundColor: '#f0f0f0' }}
          ref={stageRef}
          onClick={handleStageClick}
          onTap={handleStageClick}
        >
          <Layer>
            {links.map((link) => {
              const sourceDevice = devices.find(d => d.id === link.sourceId);
              const targetDevice = devices.find(d => d.id === link.targetId);
              if (!sourceDevice || !targetDevice) return null;
              const sourceCenter = getDeviceCenter(link.sourceId);
              const targetCenter = getDeviceCenter(link.targetId);
              return (
                <Line
                  key={link.id}
                  points={[sourceCenter.x, sourceCenter.y, targetCenter.x, targetCenter.y]}
                  stroke="black"
                  strokeWidth={2}
                  tension={0} // Straight lines
                />
              );
            })}
            {devices.map((device) => (
              <DeviceNode
                key={device.id}
                shapeProps={{ x: device.x, y: device.y }}
                name={device.name}
                onDragEnd={(e) => handleDeviceDragEnd(device.id, e)}
                onClick={() => handleDeviceClick(device.id)}
                // TODO: Add visual indication if device is selected (e.g., different stroke color)
              />
            ))}
          </Layer>
        </Stage>
      </div>
      <PropertyEditor
        selectedDevice={editingDevice}
        onUpdateDeviceProperties={handleUpdateDeviceProperties}
        onDeselectDevice={handleDeselectDevice}
      />
    </div>
  );
};

export default TopologyEditorPage;

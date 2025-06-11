// frontend/src/components/topology/PropertyEditor.jsx
import React, { useState, useEffect } from 'react';

const DEVICE_TYPES = ["Router", "Switch", "PC", "Server", "Firewall"];

const PropertyEditor = ({ selectedDevice, onUpdateDeviceProperties, onDeselectDevice }) => {
  const [properties, setProperties] = useState({
    name: '',
    device_type: DEVICE_TYPES[0],
    num_ports: 0,
    total_bandwidth: 0,
    throughput_per_port: 0,
    estimated_load: 0,
  });

  useEffect(() => {
    if (selectedDevice) {
      setProperties({
        name: selectedDevice.name || '',
        device_type: selectedDevice.type || DEVICE_TYPES[0],
        num_ports: selectedDevice.properties?.num_ports || 0, // Use optional chaining
        total_bandwidth: selectedDevice.properties?.total_bandwidth || 0,
        throughput_per_port: selectedDevice.properties?.throughput_per_port || 0,
        estimated_load: selectedDevice.properties?.estimated_load || 0,
      });
    } else {
      // Reset form when no device is selected
      setProperties({
        name: '',
        device_type: DEVICE_TYPES[0],
        num_ports: 0,
        total_bandwidth: 0,
        throughput_per_port: 0,
        estimated_load: 0,
      });
    }
  }, [selectedDevice]);

  if (!selectedDevice) {
    return <div style={{ padding: '10px', border: '1px solid #ccc', marginLeft: '10px', minWidth: '250px', height: 'fit-content'}}>Click a device to edit its properties.</div>;
  }

  const handleChange = (e) => {
    const { name, value } = e.target;
    // Convert to number if the input type is number, otherwise use string value
    const processedValue = e.target.type === 'number' ? parseFloat(value) || 0 : value;
    setProperties(prev => ({
      ...prev,
      [name]: processedValue,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onUpdateDeviceProperties(selectedDevice.id, properties);
  };

  return (
    <div style={{ padding: '10px', border: '1px solid #ccc', marginLeft: '10px', minWidth: '250px', height: 'fit-content' }}>
      <h4>Edit: {selectedDevice.name}</h4>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '5px' }}>
          <label>Name: </label>
          <input type="text" name="name" value={properties.name} onChange={handleChange} style={{width: "100%"}}/>
        </div>
        <div style={{ marginBottom: '5px' }}>
          <label>Type: </label>
          <select name="device_type" value={properties.device_type} onChange={handleChange} style={{width: "100%"}}>
            {DEVICE_TYPES.map(type => <option key={type} value={type}>{type}</option>)}
          </select>
        </div>
        <div style={{ marginBottom: '5px' }}>
          <label>Number of Ports: </label>
          <input type="number" name="num_ports" value={properties.num_ports} onChange={handleChange} style={{width: "100%"}}/>
        </div>
        <div style={{ marginBottom: '5px' }}>
          <label>Total Bandwidth (Mbps): </label>
          <input type="number" name="total_bandwidth" value={properties.total_bandwidth} onChange={handleChange} style={{width: "100%"}}/>
        </div>
        <div style={{ marginBottom: '5px' }}>
          <label>Throughput per Port (Mbps): </label>
          <input type="number" name="throughput_per_port" value={properties.throughput_per_port} onChange={handleChange} style={{width: "100%"}}/>
        </div>
        <div style={{ marginBottom: '5px' }}>
          <label>Estimated Load (Mbps): </label>
          <input type="number" name="estimated_load" value={properties.estimated_load} onChange={handleChange} style={{width: "100%"}}/>
        </div>
        <button type="submit" style={{marginTop: '10px'}}>Update Properties</button>
        <button type="button" onClick={onDeselectDevice} style={{marginTop: '10px', marginLeft: '5px'}}>Deselect</button>
      </form>
    </div>
  );
};

export default PropertyEditor;

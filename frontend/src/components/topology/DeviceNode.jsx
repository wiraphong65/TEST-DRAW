// frontend/src/components/topology/DeviceNode.jsx
import React from 'react';
import { Rect, Text, Group } from 'react-konva';

const DeviceNode = ({ shapeProps, name, onDragEnd, onClick }) => {
  return (
    <Group
      draggable
      onDragEnd={onDragEnd}
      onClick={onClick}
      x={shapeProps.x}
      y={shapeProps.y}
    >
      <Rect
        width={100}
        height={50}
        fill="lightblue"
        stroke="black"
        strokeWidth={1}
        shadowBlur={5}
      />
      <Text
        text={name}
        fontSize={14}
        fontFamily="Arial"
        fill="#333"
        width={100} // same as Rect width
        height={50} // same as Rect height
        align="center"
        verticalAlign="middle"
        // No offsetX/Y needed if text is same size as group and using these aligns
      />
    </Group>
  );
};
export default DeviceNode;

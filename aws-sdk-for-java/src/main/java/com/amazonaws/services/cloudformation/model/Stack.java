/*
 * Copyright 2010-2012 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 * 
 *  http://aws.amazon.com/apache2.0
 * 
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
package com.amazonaws.services.cloudformation.model;

/**
 * <p>
 * The Stack data type.
 * </p>
 */
public class Stack {

    /**
     * Unique identifier of the stack.
     */
    private String stackId;

    /**
     * The name associated with the stack.
     */
    private String stackName;

    /**
     * User defined description associated with the stack.
     */
    private String description;

    /**
     * A list of <code>Parameter</code> structures.
     */
    private java.util.List<Parameter> parameters;

    /**
     * Time at which the stack was created.
     */
    private java.util.Date creationTime;

    private java.util.Date lastUpdatedTime;

    /**
     * Current status of the stack.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Allowed Values: </b>CREATE_IN_PROGRESS, CREATE_FAILED, CREATE_COMPLETE, ROLLBACK_IN_PROGRESS, ROLLBACK_FAILED, ROLLBACK_COMPLETE, DELETE_IN_PROGRESS, DELETE_FAILED, DELETE_COMPLETE, UPDATE_IN_PROGRESS, UPDATE_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_COMPLETE, UPDATE_ROLLBACK_IN_PROGRESS, UPDATE_ROLLBACK_FAILED, UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_ROLLBACK_COMPLETE
     */
    private String stackStatus;

    /**
     * Success/failure message associated with the stack status.
     */
    private String stackStatusReason;

    /**
     * Boolean to enable or disable rollback on stack creation failures: <p>
     * <ul> <li><code>true</code>: disable rollback</li>
     * <li><code>false</code>: enable rollback</li> </ul>
     */
    private Boolean disableRollback;

    /**
     * SNS topic ARNs to which stack related events are published.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Length: </b>0 - 5<br/>
     */
    private java.util.List<String> notificationARNs;

    /**
     * The amount of time within which stack creation should complete.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Range: </b>1 - <br/>
     */
    private Integer timeoutInMinutes;

    /**
     * The capabilities allowed in the stack.
     */
    private java.util.List<String> capabilities;

    /**
     * A list of output structures.
     */
    private java.util.List<Output> outputs;

    /**
     * Unique identifier of the stack.
     *
     * @return Unique identifier of the stack.
     */
    public String getStackId() {
        return stackId;
    }
    
    /**
     * Unique identifier of the stack.
     *
     * @param stackId Unique identifier of the stack.
     */
    public void setStackId(String stackId) {
        this.stackId = stackId;
    }
    
    /**
     * Unique identifier of the stack.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param stackId Unique identifier of the stack.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withStackId(String stackId) {
        this.stackId = stackId;
        return this;
    }
    
    
    /**
     * The name associated with the stack.
     *
     * @return The name associated with the stack.
     */
    public String getStackName() {
        return stackName;
    }
    
    /**
     * The name associated with the stack.
     *
     * @param stackName The name associated with the stack.
     */
    public void setStackName(String stackName) {
        this.stackName = stackName;
    }
    
    /**
     * The name associated with the stack.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param stackName The name associated with the stack.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withStackName(String stackName) {
        this.stackName = stackName;
        return this;
    }
    
    
    /**
     * User defined description associated with the stack.
     *
     * @return User defined description associated with the stack.
     */
    public String getDescription() {
        return description;
    }
    
    /**
     * User defined description associated with the stack.
     *
     * @param description User defined description associated with the stack.
     */
    public void setDescription(String description) {
        this.description = description;
    }
    
    /**
     * User defined description associated with the stack.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param description User defined description associated with the stack.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withDescription(String description) {
        this.description = description;
        return this;
    }
    
    
    /**
     * A list of <code>Parameter</code> structures.
     *
     * @return A list of <code>Parameter</code> structures.
     */
    public java.util.List<Parameter> getParameters() {
        
        if (parameters == null) {
            parameters = new java.util.ArrayList<Parameter>();
        }
        return parameters;
    }
    
    /**
     * A list of <code>Parameter</code> structures.
     *
     * @param parameters A list of <code>Parameter</code> structures.
     */
    public void setParameters(java.util.Collection<Parameter> parameters) {
        if (parameters == null) {
            this.parameters = null;
            return;
        }

        java.util.List<Parameter> parametersCopy = new java.util.ArrayList<Parameter>(parameters.size());
        parametersCopy.addAll(parameters);
        this.parameters = parametersCopy;
    }
    
    /**
     * A list of <code>Parameter</code> structures.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param parameters A list of <code>Parameter</code> structures.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withParameters(Parameter... parameters) {
        if (getParameters() == null) setParameters(new java.util.ArrayList<Parameter>(parameters.length));
        for (Parameter value : parameters) {
            getParameters().add(value);
        }
        return this;
    }
    
    /**
     * A list of <code>Parameter</code> structures.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param parameters A list of <code>Parameter</code> structures.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withParameters(java.util.Collection<Parameter> parameters) {
        if (parameters == null) {
            this.parameters = null;
        } else {
            java.util.List<Parameter> parametersCopy = new java.util.ArrayList<Parameter>(parameters.size());
            parametersCopy.addAll(parameters);
            this.parameters = parametersCopy;
        }

        return this;
    }
    
    /**
     * Time at which the stack was created.
     *
     * @return Time at which the stack was created.
     */
    public java.util.Date getCreationTime() {
        return creationTime;
    }
    
    /**
     * Time at which the stack was created.
     *
     * @param creationTime Time at which the stack was created.
     */
    public void setCreationTime(java.util.Date creationTime) {
        this.creationTime = creationTime;
    }
    
    /**
     * Time at which the stack was created.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param creationTime Time at which the stack was created.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withCreationTime(java.util.Date creationTime) {
        this.creationTime = creationTime;
        return this;
    }
    
    
    /**
     * Returns the value of the LastUpdatedTime property for this object.
     *
     * @return The value of the LastUpdatedTime property for this object.
     */
    public java.util.Date getLastUpdatedTime() {
        return lastUpdatedTime;
    }
    
    /**
     * Sets the value of the LastUpdatedTime property for this object.
     *
     * @param lastUpdatedTime The new value for the LastUpdatedTime property for this object.
     */
    public void setLastUpdatedTime(java.util.Date lastUpdatedTime) {
        this.lastUpdatedTime = lastUpdatedTime;
    }
    
    /**
     * Sets the value of the LastUpdatedTime property for this object.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param lastUpdatedTime The new value for the LastUpdatedTime property for this object.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withLastUpdatedTime(java.util.Date lastUpdatedTime) {
        this.lastUpdatedTime = lastUpdatedTime;
        return this;
    }
    
    
    /**
     * Current status of the stack.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Allowed Values: </b>CREATE_IN_PROGRESS, CREATE_FAILED, CREATE_COMPLETE, ROLLBACK_IN_PROGRESS, ROLLBACK_FAILED, ROLLBACK_COMPLETE, DELETE_IN_PROGRESS, DELETE_FAILED, DELETE_COMPLETE, UPDATE_IN_PROGRESS, UPDATE_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_COMPLETE, UPDATE_ROLLBACK_IN_PROGRESS, UPDATE_ROLLBACK_FAILED, UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_ROLLBACK_COMPLETE
     *
     * @return Current status of the stack.
     *
     * @see StackStatus
     */
    public String getStackStatus() {
        return stackStatus;
    }
    
    /**
     * Current status of the stack.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Allowed Values: </b>CREATE_IN_PROGRESS, CREATE_FAILED, CREATE_COMPLETE, ROLLBACK_IN_PROGRESS, ROLLBACK_FAILED, ROLLBACK_COMPLETE, DELETE_IN_PROGRESS, DELETE_FAILED, DELETE_COMPLETE, UPDATE_IN_PROGRESS, UPDATE_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_COMPLETE, UPDATE_ROLLBACK_IN_PROGRESS, UPDATE_ROLLBACK_FAILED, UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_ROLLBACK_COMPLETE
     *
     * @param stackStatus Current status of the stack.
     *
     * @see StackStatus
     */
    public void setStackStatus(String stackStatus) {
        this.stackStatus = stackStatus;
    }
    
    /**
     * Current status of the stack.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Allowed Values: </b>CREATE_IN_PROGRESS, CREATE_FAILED, CREATE_COMPLETE, ROLLBACK_IN_PROGRESS, ROLLBACK_FAILED, ROLLBACK_COMPLETE, DELETE_IN_PROGRESS, DELETE_FAILED, DELETE_COMPLETE, UPDATE_IN_PROGRESS, UPDATE_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_COMPLETE, UPDATE_ROLLBACK_IN_PROGRESS, UPDATE_ROLLBACK_FAILED, UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_ROLLBACK_COMPLETE
     *
     * @param stackStatus Current status of the stack.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     *
     * @see StackStatus
     */
    public Stack withStackStatus(String stackStatus) {
        this.stackStatus = stackStatus;
        return this;
    }
    
    
    /**
     * Current status of the stack.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Allowed Values: </b>CREATE_IN_PROGRESS, CREATE_FAILED, CREATE_COMPLETE, ROLLBACK_IN_PROGRESS, ROLLBACK_FAILED, ROLLBACK_COMPLETE, DELETE_IN_PROGRESS, DELETE_FAILED, DELETE_COMPLETE, UPDATE_IN_PROGRESS, UPDATE_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_COMPLETE, UPDATE_ROLLBACK_IN_PROGRESS, UPDATE_ROLLBACK_FAILED, UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_ROLLBACK_COMPLETE
     *
     * @param stackStatus Current status of the stack.
     *
     * @see StackStatus
     */
    public void setStackStatus(StackStatus stackStatus) {
        this.stackStatus = stackStatus.toString();
    }
    
    /**
     * Current status of the stack.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Allowed Values: </b>CREATE_IN_PROGRESS, CREATE_FAILED, CREATE_COMPLETE, ROLLBACK_IN_PROGRESS, ROLLBACK_FAILED, ROLLBACK_COMPLETE, DELETE_IN_PROGRESS, DELETE_FAILED, DELETE_COMPLETE, UPDATE_IN_PROGRESS, UPDATE_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_COMPLETE, UPDATE_ROLLBACK_IN_PROGRESS, UPDATE_ROLLBACK_FAILED, UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS, UPDATE_ROLLBACK_COMPLETE
     *
     * @param stackStatus Current status of the stack.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     *
     * @see StackStatus
     */
    public Stack withStackStatus(StackStatus stackStatus) {
        this.stackStatus = stackStatus.toString();
        return this;
    }
    
    /**
     * Success/failure message associated with the stack status.
     *
     * @return Success/failure message associated with the stack status.
     */
    public String getStackStatusReason() {
        return stackStatusReason;
    }
    
    /**
     * Success/failure message associated with the stack status.
     *
     * @param stackStatusReason Success/failure message associated with the stack status.
     */
    public void setStackStatusReason(String stackStatusReason) {
        this.stackStatusReason = stackStatusReason;
    }
    
    /**
     * Success/failure message associated with the stack status.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param stackStatusReason Success/failure message associated with the stack status.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withStackStatusReason(String stackStatusReason) {
        this.stackStatusReason = stackStatusReason;
        return this;
    }
    
    
    /**
     * Boolean to enable or disable rollback on stack creation failures: <p>
     * <ul> <li><code>true</code>: disable rollback</li>
     * <li><code>false</code>: enable rollback</li> </ul>
     *
     * @return Boolean to enable or disable rollback on stack creation failures: <p>
     *         <ul> <li><code>true</code>: disable rollback</li>
     *         <li><code>false</code>: enable rollback</li> </ul>
     */
    public Boolean isDisableRollback() {
        return disableRollback;
    }
    
    /**
     * Boolean to enable or disable rollback on stack creation failures: <p>
     * <ul> <li><code>true</code>: disable rollback</li>
     * <li><code>false</code>: enable rollback</li> </ul>
     *
     * @param disableRollback Boolean to enable or disable rollback on stack creation failures: <p>
     *         <ul> <li><code>true</code>: disable rollback</li>
     *         <li><code>false</code>: enable rollback</li> </ul>
     */
    public void setDisableRollback(Boolean disableRollback) {
        this.disableRollback = disableRollback;
    }
    
    /**
     * Boolean to enable or disable rollback on stack creation failures: <p>
     * <ul> <li><code>true</code>: disable rollback</li>
     * <li><code>false</code>: enable rollback</li> </ul>
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param disableRollback Boolean to enable or disable rollback on stack creation failures: <p>
     *         <ul> <li><code>true</code>: disable rollback</li>
     *         <li><code>false</code>: enable rollback</li> </ul>
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withDisableRollback(Boolean disableRollback) {
        this.disableRollback = disableRollback;
        return this;
    }
    
    
    /**
     * Boolean to enable or disable rollback on stack creation failures: <p>
     * <ul> <li><code>true</code>: disable rollback</li>
     * <li><code>false</code>: enable rollback</li> </ul>
     *
     * @return Boolean to enable or disable rollback on stack creation failures: <p>
     *         <ul> <li><code>true</code>: disable rollback</li>
     *         <li><code>false</code>: enable rollback</li> </ul>
     */
    public Boolean getDisableRollback() {
        return disableRollback;
    }
    
    /**
     * SNS topic ARNs to which stack related events are published.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Length: </b>0 - 5<br/>
     *
     * @return SNS topic ARNs to which stack related events are published.
     */
    public java.util.List<String> getNotificationARNs() {
        
        if (notificationARNs == null) {
            notificationARNs = new java.util.ArrayList<String>();
        }
        return notificationARNs;
    }
    
    /**
     * SNS topic ARNs to which stack related events are published.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Length: </b>0 - 5<br/>
     *
     * @param notificationARNs SNS topic ARNs to which stack related events are published.
     */
    public void setNotificationARNs(java.util.Collection<String> notificationARNs) {
        if (notificationARNs == null) {
            this.notificationARNs = null;
            return;
        }

        java.util.List<String> notificationARNsCopy = new java.util.ArrayList<String>(notificationARNs.size());
        notificationARNsCopy.addAll(notificationARNs);
        this.notificationARNs = notificationARNsCopy;
    }
    
    /**
     * SNS topic ARNs to which stack related events are published.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Length: </b>0 - 5<br/>
     *
     * @param notificationARNs SNS topic ARNs to which stack related events are published.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withNotificationARNs(String... notificationARNs) {
        if (getNotificationARNs() == null) setNotificationARNs(new java.util.ArrayList<String>(notificationARNs.length));
        for (String value : notificationARNs) {
            getNotificationARNs().add(value);
        }
        return this;
    }
    
    /**
     * SNS topic ARNs to which stack related events are published.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Length: </b>0 - 5<br/>
     *
     * @param notificationARNs SNS topic ARNs to which stack related events are published.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withNotificationARNs(java.util.Collection<String> notificationARNs) {
        if (notificationARNs == null) {
            this.notificationARNs = null;
        } else {
            java.util.List<String> notificationARNsCopy = new java.util.ArrayList<String>(notificationARNs.size());
            notificationARNsCopy.addAll(notificationARNs);
            this.notificationARNs = notificationARNsCopy;
        }

        return this;
    }
    
    /**
     * The amount of time within which stack creation should complete.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Range: </b>1 - <br/>
     *
     * @return The amount of time within which stack creation should complete.
     */
    public Integer getTimeoutInMinutes() {
        return timeoutInMinutes;
    }
    
    /**
     * The amount of time within which stack creation should complete.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Range: </b>1 - <br/>
     *
     * @param timeoutInMinutes The amount of time within which stack creation should complete.
     */
    public void setTimeoutInMinutes(Integer timeoutInMinutes) {
        this.timeoutInMinutes = timeoutInMinutes;
    }
    
    /**
     * The amount of time within which stack creation should complete.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     * <p>
     * <b>Constraints:</b><br/>
     * <b>Range: </b>1 - <br/>
     *
     * @param timeoutInMinutes The amount of time within which stack creation should complete.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withTimeoutInMinutes(Integer timeoutInMinutes) {
        this.timeoutInMinutes = timeoutInMinutes;
        return this;
    }
    
    
    /**
     * The capabilities allowed in the stack.
     *
     * @return The capabilities allowed in the stack.
     */
    public java.util.List<String> getCapabilities() {
        
        if (capabilities == null) {
            capabilities = new java.util.ArrayList<String>();
        }
        return capabilities;
    }
    
    /**
     * The capabilities allowed in the stack.
     *
     * @param capabilities The capabilities allowed in the stack.
     */
    public void setCapabilities(java.util.Collection<String> capabilities) {
        if (capabilities == null) {
            this.capabilities = null;
            return;
        }

        java.util.List<String> capabilitiesCopy = new java.util.ArrayList<String>(capabilities.size());
        capabilitiesCopy.addAll(capabilities);
        this.capabilities = capabilitiesCopy;
    }
    
    /**
     * The capabilities allowed in the stack.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param capabilities The capabilities allowed in the stack.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withCapabilities(String... capabilities) {
        if (getCapabilities() == null) setCapabilities(new java.util.ArrayList<String>(capabilities.length));
        for (String value : capabilities) {
            getCapabilities().add(value);
        }
        return this;
    }
    
    /**
     * The capabilities allowed in the stack.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param capabilities The capabilities allowed in the stack.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withCapabilities(java.util.Collection<String> capabilities) {
        if (capabilities == null) {
            this.capabilities = null;
        } else {
            java.util.List<String> capabilitiesCopy = new java.util.ArrayList<String>(capabilities.size());
            capabilitiesCopy.addAll(capabilities);
            this.capabilities = capabilitiesCopy;
        }

        return this;
    }
    
    /**
     * A list of output structures.
     *
     * @return A list of output structures.
     */
    public java.util.List<Output> getOutputs() {
        
        if (outputs == null) {
            outputs = new java.util.ArrayList<Output>();
        }
        return outputs;
    }
    
    /**
     * A list of output structures.
     *
     * @param outputs A list of output structures.
     */
    public void setOutputs(java.util.Collection<Output> outputs) {
        if (outputs == null) {
            this.outputs = null;
            return;
        }

        java.util.List<Output> outputsCopy = new java.util.ArrayList<Output>(outputs.size());
        outputsCopy.addAll(outputs);
        this.outputs = outputsCopy;
    }
    
    /**
     * A list of output structures.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param outputs A list of output structures.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withOutputs(Output... outputs) {
        if (getOutputs() == null) setOutputs(new java.util.ArrayList<Output>(outputs.length));
        for (Output value : outputs) {
            getOutputs().add(value);
        }
        return this;
    }
    
    /**
     * A list of output structures.
     * <p>
     * Returns a reference to this object so that method calls can be chained together.
     *
     * @param outputs A list of output structures.
     *
     * @return A reference to this updated object so that method calls can be chained 
     *         together. 
     */
    public Stack withOutputs(java.util.Collection<Output> outputs) {
        if (outputs == null) {
            this.outputs = null;
        } else {
            java.util.List<Output> outputsCopy = new java.util.ArrayList<Output>(outputs.size());
            outputsCopy.addAll(outputs);
            this.outputs = outputsCopy;
        }

        return this;
    }
    
    /**
     * Returns a string representation of this object; useful for testing and
     * debugging.
     *
     * @return A string representation of this object.
     *
     * @see java.lang.Object#toString()
     */
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("{");
        if (stackId != null) sb.append("StackId: " + stackId + ", ");
        if (stackName != null) sb.append("StackName: " + stackName + ", ");
        if (description != null) sb.append("Description: " + description + ", ");
        if (parameters != null) sb.append("Parameters: " + parameters + ", ");
        if (creationTime != null) sb.append("CreationTime: " + creationTime + ", ");
        if (lastUpdatedTime != null) sb.append("LastUpdatedTime: " + lastUpdatedTime + ", ");
        if (stackStatus != null) sb.append("StackStatus: " + stackStatus + ", ");
        if (stackStatusReason != null) sb.append("StackStatusReason: " + stackStatusReason + ", ");
        if (disableRollback != null) sb.append("DisableRollback: " + disableRollback + ", ");
        if (notificationARNs != null) sb.append("NotificationARNs: " + notificationARNs + ", ");
        if (timeoutInMinutes != null) sb.append("TimeoutInMinutes: " + timeoutInMinutes + ", ");
        if (capabilities != null) sb.append("Capabilities: " + capabilities + ", ");
        if (outputs != null) sb.append("Outputs: " + outputs + ", ");
        sb.append("}");
        return sb.toString();
    }
    
    @Override
    public int hashCode() {
        final int prime = 31;
        int hashCode = 1;
        
        hashCode = prime * hashCode + ((getStackId() == null) ? 0 : getStackId().hashCode()); 
        hashCode = prime * hashCode + ((getStackName() == null) ? 0 : getStackName().hashCode()); 
        hashCode = prime * hashCode + ((getDescription() == null) ? 0 : getDescription().hashCode()); 
        hashCode = prime * hashCode + ((getParameters() == null) ? 0 : getParameters().hashCode()); 
        hashCode = prime * hashCode + ((getCreationTime() == null) ? 0 : getCreationTime().hashCode()); 
        hashCode = prime * hashCode + ((getLastUpdatedTime() == null) ? 0 : getLastUpdatedTime().hashCode()); 
        hashCode = prime * hashCode + ((getStackStatus() == null) ? 0 : getStackStatus().hashCode()); 
        hashCode = prime * hashCode + ((getStackStatusReason() == null) ? 0 : getStackStatusReason().hashCode()); 
        hashCode = prime * hashCode + ((isDisableRollback() == null) ? 0 : isDisableRollback().hashCode()); 
        hashCode = prime * hashCode + ((getNotificationARNs() == null) ? 0 : getNotificationARNs().hashCode()); 
        hashCode = prime * hashCode + ((getTimeoutInMinutes() == null) ? 0 : getTimeoutInMinutes().hashCode()); 
        hashCode = prime * hashCode + ((getCapabilities() == null) ? 0 : getCapabilities().hashCode()); 
        hashCode = prime * hashCode + ((getOutputs() == null) ? 0 : getOutputs().hashCode()); 
        return hashCode;
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null) return false;
    
        if (obj instanceof Stack == false) return false;
        Stack other = (Stack)obj;
        
        if (other.getStackId() == null ^ this.getStackId() == null) return false;
        if (other.getStackId() != null && other.getStackId().equals(this.getStackId()) == false) return false; 
        if (other.getStackName() == null ^ this.getStackName() == null) return false;
        if (other.getStackName() != null && other.getStackName().equals(this.getStackName()) == false) return false; 
        if (other.getDescription() == null ^ this.getDescription() == null) return false;
        if (other.getDescription() != null && other.getDescription().equals(this.getDescription()) == false) return false; 
        if (other.getParameters() == null ^ this.getParameters() == null) return false;
        if (other.getParameters() != null && other.getParameters().equals(this.getParameters()) == false) return false; 
        if (other.getCreationTime() == null ^ this.getCreationTime() == null) return false;
        if (other.getCreationTime() != null && other.getCreationTime().equals(this.getCreationTime()) == false) return false; 
        if (other.getLastUpdatedTime() == null ^ this.getLastUpdatedTime() == null) return false;
        if (other.getLastUpdatedTime() != null && other.getLastUpdatedTime().equals(this.getLastUpdatedTime()) == false) return false; 
        if (other.getStackStatus() == null ^ this.getStackStatus() == null) return false;
        if (other.getStackStatus() != null && other.getStackStatus().equals(this.getStackStatus()) == false) return false; 
        if (other.getStackStatusReason() == null ^ this.getStackStatusReason() == null) return false;
        if (other.getStackStatusReason() != null && other.getStackStatusReason().equals(this.getStackStatusReason()) == false) return false; 
        if (other.isDisableRollback() == null ^ this.isDisableRollback() == null) return false;
        if (other.isDisableRollback() != null && other.isDisableRollback().equals(this.isDisableRollback()) == false) return false; 
        if (other.getNotificationARNs() == null ^ this.getNotificationARNs() == null) return false;
        if (other.getNotificationARNs() != null && other.getNotificationARNs().equals(this.getNotificationARNs()) == false) return false; 
        if (other.getTimeoutInMinutes() == null ^ this.getTimeoutInMinutes() == null) return false;
        if (other.getTimeoutInMinutes() != null && other.getTimeoutInMinutes().equals(this.getTimeoutInMinutes()) == false) return false; 
        if (other.getCapabilities() == null ^ this.getCapabilities() == null) return false;
        if (other.getCapabilities() != null && other.getCapabilities().equals(this.getCapabilities()) == false) return false; 
        if (other.getOutputs() == null ^ this.getOutputs() == null) return false;
        if (other.getOutputs() != null && other.getOutputs().equals(this.getOutputs()) == false) return false; 
        return true;
    }
    
}
    
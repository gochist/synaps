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
package com.amazonaws.services.elasticbeanstalk.model.transform;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.amazonaws.AmazonClientException;
import com.amazonaws.Request;
import com.amazonaws.DefaultRequest;
import com.amazonaws.services.elasticbeanstalk.model.*;
import com.amazonaws.transform.Marshaller;
import com.amazonaws.util.StringUtils;

/**
 * Request Environment Info Request Marshaller
 */
public class RequestEnvironmentInfoRequestMarshaller implements Marshaller<Request<RequestEnvironmentInfoRequest>, RequestEnvironmentInfoRequest> {

    public Request<RequestEnvironmentInfoRequest> marshall(RequestEnvironmentInfoRequest requestEnvironmentInfoRequest) {

        if (requestEnvironmentInfoRequest == null) {
		    throw new AmazonClientException("Invalid argument passed to marshall(...)");
		}

        Request<RequestEnvironmentInfoRequest> request = new DefaultRequest<RequestEnvironmentInfoRequest>(requestEnvironmentInfoRequest, "AWSElasticBeanstalk");
        request.addParameter("Action", "RequestEnvironmentInfo");
        request.addParameter("Version", "2010-12-01");

        if (requestEnvironmentInfoRequest.getEnvironmentId() != null) {
            request.addParameter("EnvironmentId", StringUtils.fromString(requestEnvironmentInfoRequest.getEnvironmentId()));
        }
        if (requestEnvironmentInfoRequest.getEnvironmentName() != null) {
            request.addParameter("EnvironmentName", StringUtils.fromString(requestEnvironmentInfoRequest.getEnvironmentName()));
        }
        if (requestEnvironmentInfoRequest.getInfoType() != null) {
            request.addParameter("InfoType", StringUtils.fromString(requestEnvironmentInfoRequest.getInfoType()));
        }


        return request;
    }
}

/*
 * Copyright 2000-2010 JetBrains s.r.o.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.intellij.internal.statistic.persistence;

import org.jetbrains.annotations.NonNls;

public class BasicSentUsagesPersistenceComponent extends SentUsagesPersistence {

  public BasicSentUsagesPersistenceComponent() {
  }

  @NonNls
  private long mySentTime = 0;
  @NonNls
  private long myEventLogSentTime = 0;

  @Override
  public boolean isAllowed() {
    return true;
  }

  @Override
  public boolean isShowNotification() {
    return false;
  }

  @Override
  public long getLastTimeSent() {
    return mySentTime;
  }

  public void setSentTime(long time) {
    mySentTime = time;
  }

  public long getEventLogLastTimeSent() {
    return myEventLogSentTime;
  }

  public void setEventLogSentTime(long time) {
    myEventLogSentTime = time;
  }
}
